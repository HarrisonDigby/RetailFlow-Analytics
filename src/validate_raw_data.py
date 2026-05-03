from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path("data/raw")

# Map each logical dataset name to the raw CSV file expected in data/raw.
REQUIRED_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "ad_spend": "ad_spend.csv",
    "refunds": "refunds.csv",
}

# Define the minimum required schema for each raw dataset.
# If a source export changes unexpectedly, these checks should fail before loading.
REQUIRED_COLUMNS = {
    "customers": [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "country",
        "signup_date",
    ],
    "products": [
        "product_id",
        "product_name",
        "category",
        "unit_price",
        "unit_cost",
    ],
    "orders": [
        "order_id",
        "customer_id",
        "product_id",
        "order_date",
        "channel",
        "quantity",
        "unit_price",
        "status",
    ],
    "ad_spend": [
        "date",
        "platform",
        "campaign",
        "spend",
        "clicks",
        "impressions",
    ],
    "refunds": [
        "refund_id",
        "order_id",
        "refund_date",
        "refund_reason",
    ],
}


# Load the raw source files so all validation checks can work from the same datasets.
def load_raw_data() -> dict[str, pd.DataFrame]:
    """Load all required raw CSV files into pandas DataFrames."""
    datasets = {}

    for dataset_name, filename in REQUIRED_FILES.items():
        file_path = RAW_DATA_DIR / filename

        # Stop immediately if an expected source file has not been generated.
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required file: {file_path}")

        # Store each dataset by business name rather than filename.
        datasets[dataset_name] = pd.read_csv(file_path)

    return datasets


# Check that the raw files contain the columns needed by later warehouse models.
def check_required_columns(datasets: dict[str, pd.DataFrame]) -> list[str]:
    """Return errors for any raw dataset missing required columns."""
    errors = []

    for dataset_name, required_columns in REQUIRED_COLUMNS.items():
        dataframe = datasets[dataset_name]

        # Compare the actual source columns with the schema required downstream.
        missing_columns = set(required_columns) - set(dataframe.columns)

        if missing_columns:
            errors.append(
                f"{dataset_name} is missing columns: {sorted(missing_columns)}"
            )

    return errors


# Check that each main dataset has reliable ID columns for joins and lookups.
def check_primary_keys(datasets: dict[str, pd.DataFrame]) -> list[str]:
    """Return errors for null or duplicated primary key values."""
    errors = []

    # These columns should uniquely identify records in their datasets.
    primary_keys = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "refunds": "refund_id",
    }

    for dataset_name, primary_key in primary_keys.items():
        dataframe = datasets[dataset_name]

        # Null IDs would break joins and make records impossible to identify.
        if dataframe[primary_key].isna().any():
            errors.append(f"{dataset_name}.{primary_key} contains null values")

        # Duplicate IDs would create ambiguous joins and unreliable metrics.
        if dataframe[primary_key].duplicated().any():
            errors.append(f"{dataset_name}.{primary_key} contains duplicate values")

    return errors


# Check simple numeric business rules before the data enters the warehouse.
def check_numeric_values(datasets: dict[str, pd.DataFrame]) -> list[str]:
    """Return errors for invalid negative values in numeric business fields."""
    errors = []

    # Define simple business rules for numeric fields in the raw data.
    checks = [
        ("products", "unit_price", 0),
        ("products", "unit_cost", 0),
        ("orders", "quantity", 0),
        ("orders", "unit_price", 0),
        ("ad_spend", "spend", 0),
        ("ad_spend", "clicks", 0),
        ("ad_spend", "impressions", 0),
    ]

    for dataset_name, column, minimum_value in checks:
        dataframe = datasets[dataset_name]

        # Negative prices, quantities, spend, clicks, or impressions are invalid.
        if (dataframe[column] < minimum_value).any():
            errors.append(
                f"{dataset_name}.{column} contains values below {minimum_value}"
            )

    return errors


# Check that IDs referenced across datasets actually exist in the parent tables.
def check_referential_integrity(datasets: dict[str, pd.DataFrame]) -> list[str]:
    """Return errors for broken relationships between raw datasets."""
    errors = []

    # Create lookup sets for the valid IDs that other datasets should reference.
    customer_ids = set(datasets["customers"]["customer_id"])
    product_ids = set(datasets["products"]["product_id"])
    order_ids = set(datasets["orders"]["order_id"])

    # Orders should only reference existing customers and products.
    invalid_order_customers = set(datasets["orders"]["customer_id"]) - customer_ids
    invalid_order_products = set(datasets["orders"]["product_id"]) - product_ids

    # Refunds should only reference existing orders.
    invalid_refund_orders = set(datasets["refunds"]["order_id"]) - order_ids

    if invalid_order_customers:
        errors.append("orders contains customer_id values not found in customers")

    if invalid_order_products:
        errors.append("orders contains product_id values not found in products")

    if invalid_refund_orders:
        errors.append("refunds contains order_id values not found in orders")

    return errors


# Check that refund records make sense compared with their original order dates.
def check_refund_dates(datasets: dict[str, pd.DataFrame]) -> list[str]:
    """Return errors for refunds dated before their original orders."""
    errors = []

    # Keep only the columns needed to compare order dates with refund dates.
    orders = datasets["orders"][["order_id", "order_date"]].copy()
    refunds = datasets["refunds"][["order_id", "refund_date"]].copy()

    # Convert date strings into datetime values so they can be compared properly.
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    refunds["refund_date"] = pd.to_datetime(refunds["refund_date"])

    # Attach the original order date to each refund.
    refund_dates = refunds.merge(orders, on="order_id", how="left")

    # A refund before the original order date is logically invalid.
    invalid_refund_dates = refund_dates[
        refund_dates["refund_date"] < refund_dates["order_date"]
    ]

    if not invalid_refund_dates.empty:
        errors.append("refunds contains refund_date values before order_date")

    return errors


# Run every raw-data validation check as a single pipeline quality gate.
def run_validation() -> None:
    """Run all raw data validation checks and stop the pipeline if any fail."""
    datasets = load_raw_data()

    # Collect all validation failures rather than stopping at the first issue.
    errors = []
    errors.extend(check_required_columns(datasets))
    errors.extend(check_primary_keys(datasets))
    errors.extend(check_numeric_values(datasets))
    errors.extend(check_referential_integrity(datasets))
    errors.extend(check_refund_dates(datasets))

    # Fail the script if any validation check found a data quality issue.
    if errors:
        print("Raw data validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Raw data validation passed.")
    print(f"Validated {len(datasets)} raw datasets.")


if __name__ == "__main__":
    run_validation()