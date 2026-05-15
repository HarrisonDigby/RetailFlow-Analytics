-- Use the project warehouse and database.
USE WAREHOUSE retailflow_wh;
USE DATABASE retailflow_db;

-- Clear existing raw tables so this load can be safely rerun.
TRUNCATE TABLE raw.customers;
TRUNCATE TABLE raw.products;
TRUNCATE TABLE raw.orders;
TRUNCATE TABLE raw.ad_spend;
TRUNCATE TABLE raw.refunds;

-- Load customer data from S3 into the raw customer table.
COPY INTO raw.customers
FROM @raw.retailflow_s3_stage/customers/customers.csv
FILE_FORMAT = raw.retailflow_s3_csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- Load product data from S3 into the raw product table.
COPY INTO raw.products
FROM @raw.retailflow_s3_stage/products/products.csv
FILE_FORMAT = raw.retailflow_s3_csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- Load order data from S3 into the raw order table.
COPY INTO raw.orders
FROM @raw.retailflow_s3_stage/orders/orders.csv
FILE_FORMAT = raw.retailflow_s3_csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- Load advertising spend data from S3 into the raw ad spend table.
COPY INTO raw.ad_spend
FROM @raw.retailflow_s3_stage/ad_spend/ad_spend.csv
FILE_FORMAT = raw.retailflow_s3_csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- Load refund data from S3 into the raw refunds table.
COPY INTO raw.refunds
FROM @raw.retailflow_s3_stage/refunds/refunds.csv
FILE_FORMAT = raw.retailflow_s3_csv_format
ON_ERROR = 'ABORT_STATEMENT';

-- Confirm raw table row counts after loading from S3.
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM raw.customers
UNION ALL
SELECT 'products', COUNT(*) FROM raw.products
UNION ALL
SELECT 'orders', COUNT(*) FROM raw.orders
UNION ALL
SELECT 'ad_spend', COUNT(*) FROM raw.ad_spend
UNION ALL
SELECT 'refunds', COUNT(*) FROM raw.refunds;