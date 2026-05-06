-- Use the project warehouse and database for this setup script.
USE WAREHOUSE retailflow_wh;
USE DATABASE retailflow_db;

-- Create the raw customers table.
-- This stores customer records loaded from the processed customers CSV.
CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id INTEGER,
    first_name STRING,
    last_name STRING,
    email STRING,
    country STRING,
    signup_date DATE
);

-- Create the raw products table.
-- This stores product catalogue records, including price, cost, and margin.
CREATE TABLE IF NOT EXISTS raw.products (
    product_id INTEGER,
    product_name STRING,
    category STRING,
    unit_price NUMBER(10, 2),
    unit_cost NUMBER(10, 2),
    unit_margin NUMBER(10, 2)
);

-- Create the raw orders table.
-- This stores order-line records from all sales channels.
CREATE TABLE IF NOT EXISTS raw.orders (
    order_id INTEGER,
    customer_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    channel STRING,
    quantity INTEGER,
    unit_price NUMBER(10, 2),
    status STRING,
    gross_revenue NUMBER(10, 2)
);

-- Create the raw advertising spend table.
-- This stores daily paid media performance by platform and campaign.
CREATE TABLE IF NOT EXISTS raw.ad_spend (
    date DATE,
    platform STRING,
    campaign STRING,
    spend NUMBER(10, 2),
    clicks INTEGER,
    impressions INTEGER,
    cost_per_click NUMBER(10, 2),
    click_through_rate NUMBER(10, 4)
);

-- Create the raw refunds table.
-- This stores refund records linked back to original orders.
CREATE TABLE IF NOT EXISTS raw.refunds (
    refund_id INTEGER,
    order_id INTEGER,
    refund_date DATE,
    refund_reason STRING
);

-- Confirm that the raw tables now exist.
SHOW TABLES IN SCHEMA raw;