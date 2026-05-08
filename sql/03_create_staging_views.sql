-- Use the project warehouse and database for this setup script.
USE WAREHOUSE retailflow_wh;
USE DATABASE retailflow_db;

-- Create a cleaned customer staging view.
-- This provides standardised customer fields for downstream marts models.
CREATE OR REPLACE VIEW staging.stg_customers AS
SELECT
    customer_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    LOWER(TRIM(email)) AS email,
    TRIM(country) AS country,
    signup_date
FROM raw.customers;

-- Create a cleaned product staging view.
-- This provides product catalogue fields and reusable margin calculations.
CREATE OR REPLACE VIEW staging.stg_products AS
SELECT
    product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    unit_price,
    unit_cost,
    unit_margin,
    ROUND(unit_margin / NULLIF(unit_price, 0), 4) AS margin_rate
FROM raw.products;

-- Create a cleaned order staging view.
-- This standardises sales-channel and status fields before fact modelling.
CREATE OR REPLACE VIEW staging.stg_orders AS
SELECT
    order_id,
    customer_id,
    product_id,
    order_date,
    TRIM(channel) AS sales_channel,
    quantity,
    unit_price,
    status,
    gross_revenue,
    CASE
        WHEN status = 'completed' THEN gross_revenue
        ELSE 0 -- Only completed orders contribute to net sales revenue in this simplified model.
    END AS net_sales_revenue
FROM raw.orders;

-- Create a cleaned advertising spend staging view.
-- This standardises paid media fields before marketing reporting models.
CREATE OR REPLACE VIEW staging.stg_ad_spend AS
SELECT
    date AS spend_date,
    TRIM(platform) AS platform,
    TRIM(campaign) AS campaign,
    spend,
    clicks,
    impressions,
    cost_per_click,
    click_through_rate
FROM raw.ad_spend;

-- Create a cleaned refund staging view.
-- This standardises refund records before they are linked into order models.
CREATE OR REPLACE VIEW staging.stg_refunds AS
SELECT
    refund_id,
    order_id,
    refund_date,
    TRIM(refund_reason) AS refund_reason
FROM raw.refunds;

-- Confirm that the staging views now exist.
SHOW VIEWS IN SCHEMA staging;