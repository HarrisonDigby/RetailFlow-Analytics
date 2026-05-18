from pathlib import Path
import os

import snowflake.connector
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
S3_LOAD_SQL_FILE = PROJECT_ROOT / "sql" / "07_load_raw_tables_from_s3.sql"


# Create a Snowflake connection using credentials stored in the local .env file.
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


# Run each SQL statement in the S3-to-Snowflake load file.
def run_snowflake_s3_load() -> None:
    """Reload Snowflake RAW tables from the S3 external stage."""
    print("Starting Snowflake S3 load...")

    if not S3_LOAD_SQL_FILE.exists():
        raise FileNotFoundError(f"Missing SQL file: {S3_LOAD_SQL_FILE}")

    sql_text = S3_LOAD_SQL_FILE.read_text(encoding="utf-8")

    statements = [
        statement.strip()
        for statement in sql_text.split(";")
        if statement.strip()
    ]

    connection = get_snowflake_connection()

    try:
        cursor = connection.cursor()

        for statement in statements:
            cursor.execute(statement)

            if cursor.description:
                rows = cursor.fetchall()

                for row in rows:
                    print(row)

    finally:
        connection.close()

    print("Snowflake S3 load completed.")


if __name__ == "__main__":
    run_snowflake_s3_load()