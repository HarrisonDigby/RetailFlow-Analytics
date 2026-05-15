-- Use the project warehouse and database for this setup script.
USE WAREHOUSE retailflow_wh;
USE DATABASE retailflow_db;

-- Create a CSV file format for files loaded from S3.
CREATE FILE FORMAT IF NOT EXISTS raw.retailflow_s3_csv_format
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL', 'null')
    DATE_FORMAT = 'AUTO';

-- Create an external stage pointing to the S3 processed-data folder.
CREATE STAGE IF NOT EXISTS raw.retailflow_s3_stage
    URL = 's3://retailflow-analytics-harrison/processed/'
    CREDENTIALS = (
        AWS_KEY_ID = '<AWS_ACCESS_KEY_ID>'
        AWS_SECRET_KEY = '<AWS_SECRET_ACCESS_KEY>'
    )
    FILE_FORMAT = raw.retailflow_s3_csv_format;

-- Confirm Snowflake can see the files in the S3 stage.
LIST @raw.retailflow_s3_stage;