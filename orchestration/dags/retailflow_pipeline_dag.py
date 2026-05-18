from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/project"


# Define the Airflow DAG that orchestrates the RetailFlow pipeline.
with DAG(
    dag_id="retailflow_pipeline",
    description="Run the RetailFlow data pipeline from data generation to dbt tests.",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["retailflow", "data-engineering"],
) as dag:

    # Generate realistic raw retail source data.
    generate_data = BashOperator(
        task_id="generate_data",
        bash_command=f"cd {PROJECT_DIR} && python src/generate_data.py",
    )

    # Validate the generated raw data before it is prepared or uploaded.
    validate_raw_data = BashOperator(
        task_id="validate_raw_data",
        bash_command=f"cd {PROJECT_DIR} && python src/validate_raw_data.py",
    )

    # Prepare standardised CSV files for warehouse loading.
    prepare_data = BashOperator(
        task_id="prepare_data",
        bash_command=f"cd {PROJECT_DIR} && python src/prepare_data.py",
    )

    # Upload processed CSV files to the AWS S3 data lake.
    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command=f"cd {PROJECT_DIR} && python src/upload_to_s3.py",
    )

    # Load Snowflake RAW tables from files stored in S3.
    load_snowflake_from_s3 = BashOperator(
        task_id="load_snowflake_from_s3",
        bash_command=f"cd {PROJECT_DIR} && python src/run_snowflake_s3_load.py",
    )

    # Build dbt staging views and marts tables in Snowflake.
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT_DIR}/dbt_retailflow && dbt run",
    )

    # Run dbt data quality tests across staging and marts models.
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT_DIR}/dbt_retailflow && dbt test",
    )

    (
        generate_data
        >> validate_raw_data
        >> prepare_data
        >> upload_to_s3
        >> load_snowflake_from_s3
        >> dbt_run
        >> dbt_test
    )