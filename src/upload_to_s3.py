from pathlib import Path
import os

import boto3
from dotenv import load_dotenv


PROCESSED_DATA_DIR = Path("data/processed")

# Map local processed CSV files to their target S3 object paths.
S3_UPLOAD_CONFIG = {
    "customers": {
        "local_file": "customers.csv",
        "s3_key": "processed/customers/customers.csv",
    },
    "products": {
        "local_file": "products.csv",
        "s3_key": "processed/products/products.csv",
    },
    "orders": {
        "local_file": "orders.csv",
        "s3_key": "processed/orders/orders.csv",
    },
    "ad_spend": {
        "local_file": "ad_spend.csv",
        "s3_key": "processed/ad_spend/ad_spend.csv",
    },
    "refunds": {
        "local_file": "refunds.csv",
        "s3_key": "processed/refunds/refunds.csv",
    },
}


# Create an S3 client using credentials stored in the local .env file.
def get_s3_client():
    """Create a boto3 S3 client using environment variables."""
    load_dotenv()

    return boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_DEFAULT_REGION"],
    )


# Upload one processed CSV file to its matching S3 object path.
def upload_file_to_s3(s3_client, bucket_name: str, local_path: Path, s3_key: str) -> None:
    """Upload a local file into the project S3 bucket."""
    if not local_path.exists():
        raise FileNotFoundError(f"Missing processed file: {local_path}")

    s3_client.upload_file(
        Filename=str(local_path),
        Bucket=bucket_name,
        Key=s3_key,
    )


# Run the full processed-files-to-S3 upload step.
def run_upload() -> None:
    """Upload all processed CSV files to the S3 data lake."""
    load_dotenv()

    bucket_name = os.environ["S3_BUCKET_NAME"]
    s3_client = get_s3_client()

    for dataset_name, config in S3_UPLOAD_CONFIG.items():
        local_path = PROCESSED_DATA_DIR / config["local_file"]
        s3_key = config["s3_key"]

        upload_file_to_s3(s3_client, bucket_name, local_path, s3_key)

        print(f"Uploaded {dataset_name} to s3://{bucket_name}/{s3_key}")

    print("S3 upload completed.")


if __name__ == "__main__":
    run_upload()