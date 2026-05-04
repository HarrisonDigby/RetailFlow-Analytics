from pathlib import Path

import snowflake.connector
from dotenv import load_dotenv
import os


PROCESSED_DATA_DIR = Path("data/processed")
SNOWFLAKE_STAGE = "raw.retailflow_internal_stage"


# Map local processed CSV files to their target Snowflake raw tables.
TABLE_LOAD_CONFIG = {
    "customers": {
        "file": "customers.csv",
        "table": "raw.customers",
    },
    "products": {
        "file": "products.csv",
        "table": "raw.products",
    },
    "orders": {
        "file": "orders.csv",
        "table": "raw.orders",
    },
    "ad_spend": {
        "file": "ad_spend.csv",
        "table": "raw.ad_spend",
    },
    "refunds": {
        "file": "refunds.csv",
        "table": "raw.refunds",
    },
}


# Load Snowflake connection details from the local .env file.
def get_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    """Create a Snowflake connection using environment variables."""
    load_dotenv()

    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


# Create the internal Snowflake stage and CSV file format used for loading files.
def create_stage_and_file_format(cursor) -> None:
    """Create the Snowflake loading stage and CSV file format if they do not exist."""
    cursor.execute(
        """
        CREATE FILE FORMAT IF NOT EXISTS raw.retailflow_csv_format
            TYPE = CSV
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            NULL_IF = ('', 'NULL', 'null')
            DATE_FORMAT = 'AUTO';
        """
    )

    cursor.execute(
        """
        CREATE STAGE IF NOT EXISTS raw.retailflow_internal_stage
            FILE_FORMAT = raw.retailflow_csv_format;
        """
    )


# Remove existing staged files so each pipeline run starts from a clean loading area.
def clear_stage(cursor) -> None:
    """Remove files currently stored in the internal Snowflake stage."""
    cursor.execute(f"REMOVE @{SNOWFLAKE_STAGE}")


# Upload one local processed CSV file into the Snowflake internal stage.
def upload_file_to_stage(cursor, file_path: Path) -> None:
    """Upload a local CSV file to the Snowflake internal stage."""
    cursor.execute(
        f"PUT file://{file_path.as_posix()} @{SNOWFLAKE_STAGE} "
        "AUTO_COMPRESS = TRUE OVERWRITE = TRUE"
    )


# Load a staged CSV file into its matching raw Snowflake table.
def copy_file_into_table(cursor, staged_filename: str, table_name: str) -> None:
    """Load a staged CSV file into a Snowflake table using COPY INTO."""
    cursor.execute(
        f"""
        COPY INTO {table_name}
        FROM @{SNOWFLAKE_STAGE}/{staged_filename}.gz
        FILE_FORMAT = raw.retailflow_csv_format
        ON_ERROR = 'ABORT_STATEMENT';
        """
    )


# Empty raw tables before reloading them so reruns do not duplicate records.
def truncate_raw_tables(cursor) -> None:
    """Clear existing rows from raw tables before loading fresh data."""
    for config in TABLE_LOAD_CONFIG.values():
        cursor.execute(f"TRUNCATE TABLE {config['table']}")


# Run the full processed-CSV-to-Snowflake loading step.
def run_load() -> None:
    """Upload processed CSV files to Snowflake and load them into raw tables."""
    connection = get_snowflake_connection()

    try:
        cursor = connection.cursor()

        create_stage_and_file_format(cursor)
        clear_stage(cursor)
        truncate_raw_tables(cursor)

        for dataset_name, config in TABLE_LOAD_CONFIG.items():
            file_path = PROCESSED_DATA_DIR / config["file"]

            if not file_path.exists():
                raise FileNotFoundError(f"Missing processed file: {file_path}")

            upload_file_to_stage(cursor, file_path)
            copy_file_into_table(cursor, config["file"], config["table"])

            print(f"Loaded {dataset_name} into {config['table']}")

        print("Snowflake raw data load completed.")

    finally:
        connection.close()


if __name__ == "__main__":
    run_load()