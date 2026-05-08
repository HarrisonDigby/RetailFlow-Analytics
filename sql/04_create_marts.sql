-- Use the project warehouse and database for this setup script.
USE WAREHOUSE retailflow_wh;
USE DATABASE retailflow_db;

-- Create a customer dimension table for reporting.
CREATE OR REPLACE TABLE marts.dim_customers AS
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    country,
    signup_date
FROM staging.stg_customers;

-- Create a product dimension table for reporting.
CREATE OR REPLACE TABLE marts.dim_products AS
SELECT
    product_id,
    product_name,
    category,
    unit_price,
    unit_cost,
    unit_margin,
    margin_rate
FROM staging.stg_products;

-- Create a date dimension table from all relevant business dates.
CREATE OR REPLACE TABLE marts.dim_date AS
WITH all_dates AS (
    SELECT order_date AS date_day FROM staging.stg_orders
    UNION
    SELECT spend_date AS date_day FROM staging.stg_ad_spend
    UNION
    SELECT refund_date AS date_day FROM staging.stg_refunds
)

SELECT
    date_day,
    YEAR(date_day) AS year,
    QUARTER(date_day) AS quarter,
    MONTH(date_day) AS month,
    MONTHNAME(date_day) AS month_name,
    WEEK(date_day) AS week_of_year,
    DAYOFMONTH(date_day) AS day_of_month,
    DAYOFWEEK(date_day) AS day_of_week
FROM all_dates;

-- Create an order fact table for sales reporting.
CREATE OR REPLACE TABLE marts.fact_orders AS
SELECT
    orders.order_id,
    orders.customer_id,
    orders.product_id,
    orders.order_date,
    orders.sales_channel,
    orders.quantity,
    orders.unit_price,
    products.unit_cost,
    orders.gross_revenue,
    orders.net_sales_revenue,
    CASE
        WHEN orders.status = 'refunded' THEN orders.gross_revenue
        ELSE 0
    END AS refunded_revenue,
    CASE
        WHEN orders.status = 'cancelled' THEN orders.gross_revenue
        ELSE 0
    END AS cancelled_revenue,
    orders.status,
    CASE
        WHEN orders.status = 'completed' THEN ROUND(orders.quantity * products.unit_cost, 2)
        ELSE 0
    END AS total_cost,
    CASE
        WHEN orders.status = 'completed' THEN ROUND(orders.net_sales_revenue - (orders.quantity * products.unit_cost), 2)
        ELSE 0
    END AS gross_profit
FROM staging.stg_orders AS orders
LEFT JOIN staging.stg_products AS products
    ON orders.product_id = products.product_id;

-- Create an advertising spend fact table for marketing reporting.
CREATE OR REPLACE TABLE marts.fact_ad_spend AS
SELECT
    spend_date,
    platform,
    campaign,
    spend,
    clicks,
    impressions,
    cost_per_click,
    click_through_rate
FROM staging.stg_ad_spend;

-- Create a refund fact table for refund reporting.
CREATE OR REPLACE TABLE marts.fact_refunds AS
SELECT
    refunds.refund_id,
    refunds.order_id,
    orders.customer_id,
    orders.product_id,
    refunds.refund_date,
    refunds.refund_reason,
    orders.gross_revenue AS refund_order_value
FROM staging.stg_refunds AS refunds
LEFT JOIN staging.stg_orders AS orders
    ON refunds.order_id = orders.order_id;

-- Confirm that the marts tables now exist.
SHOW TABLES IN SCHEMA marts;