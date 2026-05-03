from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


# Define the raw files that will be standardised for warehouse loading.
SOURCE_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "ad_spend": "ad_spend.csv",
    "refunds": "refunds.csv",
}


# Load each raw CSV into pandas so it can be prepared consistently.
def load_raw_data() -> dict[str, pd.DataFrame]:
    """Load raw CSV files into pandas DataFrames."""
    datasets = {}

    for dataset_name, filename in SOURCE_FILES.items():
        file_path = RAW_DATA_DIR / filename
        datasets[dataset_name] = pd.read_csv(file_path)

    return datasets


# Standardise customer data types and text fields before warehouse loading.
def prepare_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Prepare customer records for the processed data layer."""
    prepared = customers.copy()

    # Convert IDs into integers so joins behave consistently in the warehouse.
    prepared["customer_id"] = prepared["customer_id"].astype(int)

    # Convert signup dates into a consistent ISO date format.
    prepared["signup_date"] = pd.to_datetime(prepared["signup_date"]).dt.date

    # Standardise text fields that may be used for grouping or filtering.
    prepared["country"] = prepared["country"].str.strip()

    return prepared


# Standardise product data and calculate basic product margin fields.
def prepare_products(products: pd.DataFrame) -> pd.DataFrame:
    """Prepare product records for the processed data layer."""
    prepared = products.copy()

    # Convert identifiers and financial columns into reliable numeric types.
    prepared["product_id"] = prepared["product_id"].astype(int)
    prepared["unit_price"] = prepared["unit_price"].astype(float).round(2)
    prepared["unit_cost"] = prepared["unit_cost"].astype(float).round(2)

    # Add a simple margin field that can be reused in warehouse models.
    prepared["unit_margin"] = (prepared["unit_price"] - prepared["unit_cost"]).round(2)

    # Standardise product text fields before grouping in analytics models.
    prepared["product_name"] = prepared["product_name"].str.strip()
    prepared["category"] = prepared["category"].str.strip()

    return prepared


# Standardise order data and calculate row-level revenue.
def prepare_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Prepare order records for the processed data layer."""
    prepared = orders.copy()

    # Convert IDs and quantities into integer types for warehouse joins and metrics.
    prepared["order_id"] = prepared["order_id"].astype(int)
    prepared["customer_id"] = prepared["customer_id"].astype(int)
    prepared["product_id"] = prepared["product_id"].astype(int)
    prepared["quantity"] = prepared["quantity"].astype(int)

    # Convert order dates into a consistent ISO date format.
    prepared["order_date"] = pd.to_datetime(prepared["order_date"]).dt.date

    # Standardise financial values and calculate gross revenue per order row.
    prepared["unit_price"] = prepared["unit_price"].astype(float).round(2)
    prepared["gross_revenue"] = (
        prepared["quantity"] * prepared["unit_price"]
    ).round(2)

    # Standardise categorical fields for cleaner grouping later.
    prepared["channel"] = prepared["channel"].str.strip()
    prepared["status"] = prepared["status"].str.strip().str.lower()

    return prepared


# Standardise ad spend data and calculate simple marketing efficiency metrics.
def prepare_ad_spend(ad_spend: pd.DataFrame) -> pd.DataFrame:
    """Prepare advertising spend records for the processed data layer."""
    prepared = ad_spend.copy()

    # Convert dates and numeric marketing fields into consistent types.
    prepared["date"] = pd.to_datetime(prepared["date"]).dt.date
    prepared["spend"] = prepared["spend"].astype(float).round(2)
    prepared["clicks"] = prepared["clicks"].astype(int)
    prepared["impressions"] = prepared["impressions"].astype(int)

    # Calculate simple ad metrics that are useful for quality checks and reporting.
    prepared["cost_per_click"] = (
        prepared["spend"] / prepared["clicks"].replace(0, pd.NA)
    ).round(2)
    prepared["click_through_rate"] = (
        prepared["clicks"] / prepared["impressions"].replace(0, pd.NA)
    ).round(4)

    # Standardise marketing text fields for later grouping.
    prepared["platform"] = prepared["platform"].str.strip()
    prepared["campaign"] = prepared["campaign"].str.strip()

    return prepared


# Standardise refund data before linking it back to orders in the warehouse.
def prepare_refunds(refunds: pd.DataFrame) -> pd.DataFrame:
    """Prepare refund records for the processed data layer."""
    prepared = refunds.copy()

    # Convert identifiers and refund dates into consistent types.
    prepared["refund_id"] = prepared["refund_id"].astype(int)
    prepared["order_id"] = prepared["order_id"].astype(int)
    prepared["refund_date"] = pd.to_datetime(prepared["refund_date"]).dt.date

    # Standardise refund reasons for cleaner reporting.
    prepared["refund_reason"] = prepared["refund_reason"].str.strip()

    return prepared


# Save each prepared DataFrame as a processed CSV file.
def save_processed_data(datasets: dict[str, pd.DataFrame]) -> None:
    """Write prepared datasets to the processed data directory."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for dataset_name, dataframe in datasets.items():
        output_path = PROCESSED_DATA_DIR / f"{dataset_name}.csv"
        dataframe.to_csv(output_path, index=False)


# Run the full raw-to-processed preparation step.
def run_preparation() -> None:
    """Prepare all raw datasets and save processed CSV outputs."""
    raw_datasets = load_raw_data()

    processed_datasets = {
        "customers": prepare_customers(raw_datasets["customers"]),
        "products": prepare_products(raw_datasets["products"]),
        "orders": prepare_orders(raw_datasets["orders"]),
        "ad_spend": prepare_ad_spend(raw_datasets["ad_spend"]),
        "refunds": prepare_refunds(raw_datasets["refunds"]),
    }

    save_processed_data(processed_datasets)

    print("Prepared data files created:")
    for dataset_name in processed_datasets:
        print(f"- data/processed/{dataset_name}.csv")


if __name__ == "__main__":
    run_preparation()