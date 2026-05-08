-- Use the project warehouse and database for this setup script.
USE WAREHOUSE retailflow_wh;
USE DATABASE retailflow_db;

-- Create a customer dimension table for reporting.
-- Dimension tables describe business entities used to filter and group facts.
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
-- This table provides product attributes used to analyse sales performance.
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
-- This supports time-based filtering, grouping, and reporting.
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
-- Fact tables store measurable business events and link to dimension tables.
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
    ROUND(orders.quantity * products.unit_cost, 2) AS total_cost,
    ROUND(orders.net_sales_revenue - (orders.quantity * products.unit_cost), 2) AS gross_profit
FROM staging.stg_orders AS orders
LEFT JOIN staging.stg_products AS products
    ON orders.product_id = products.product_id;

-- Create an advertising spend fact table for marketing reporting.
-- This keeps paid media metrics in a business-ready reporting table.
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
-- This can be linked back to orders for refund rate and product analysis.
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