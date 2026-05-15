from pathlib import Path
import os
import subprocess
import sys

import snowflake.connector
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt_retailflow"
S3_LOAD_SQL_FILE = PROJECT_ROOT / "sql" / "07_load_raw_tables_from_s3.sql"


# Run one Python script as a pipeline step.
def run_python_script(script_path: Path) -> None:
    """Run a Python script and stop the pipeline if it fails."""
    print(f"\nRunning Python step: {script_path.name}")

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )


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


# Run the Snowflake SQL file that reloads RAW tables from the S3 external stage.
def run_snowflake_sql_file(sql_file_path: Path) -> None:
    """Run each SQL statement in a Snowflake SQL file."""
    print(f"\nRunning Snowflake SQL step: {sql_file_path.name}")

    if not sql_file_path.exists():
        raise FileNotFoundError(f"Missing SQL file: {sql_file_path}")

    sql_text = sql_file_path.read_text(encoding="utf-8")

    # Split the SQL file into individual statements.
    # This works for this project because the SQL file uses simple semicolon-separated statements.
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

            # Print result rows for SELECT statements so row counts are visible.
            if cursor.description:
                rows = cursor.fetchall()

                for row in rows:
                    print(row)

    finally:
        connection.close()


# Run a dbt command inside the dbt project folder.
def run_dbt_command(command: list[str]) -> None:
    """Run a dbt command and stop the pipeline if it fails."""
    print(f"\nRunning dbt step: {' '.join(command)}")

    subprocess.run(
        command,
        cwd=DBT_PROJECT_DIR,
        check=True,
    )


# Run the full local-to-S3-to-Snowflake-to-dbt pipeline.
def run_pipeline() -> None:
    """Run the complete RetailFlow data pipeline."""
    print("Starting RetailFlow pipeline...")

    run_python_script(PROJECT_ROOT / "src" / "generate_data.py")
    run_python_script(PROJECT_ROOT / "src" / "validate_raw_data.py")
    run_python_script(PROJECT_ROOT / "src" / "prepare_data.py")
    run_python_script(PROJECT_ROOT / "src" / "upload_to_s3.py")

    run_snowflake_sql_file(S3_LOAD_SQL_FILE)

    run_dbt_command(["dbt", "run"])
    run_dbt_command(["dbt", "test"])

    print("\nRetailFlow pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()