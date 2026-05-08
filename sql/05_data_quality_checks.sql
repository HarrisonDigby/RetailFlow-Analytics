-- Use the project warehouse and database for this data quality script.
USE WAREHOUSE retailflow_wh;
USE DATABASE retailflow_db;

-- Return all data quality checks as one result set.
-- Each row represents one check, its status, and the number of failing records.
WITH checks AS (

    -- Check that the customer dimension contains rows.
    SELECT
        'dim_customers_not_empty' AS check_name,
        COUNT(*) = 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Table should contain at least one row' AS check_description
    FROM marts.dim_customers

    UNION ALL

    -- Check that the product dimension contains rows.
    SELECT
        'dim_products_not_empty' AS check_name,
        COUNT(*) = 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Table should contain at least one row' AS check_description
    FROM marts.dim_products

    UNION ALL

    -- Check that the date dimension contains rows.
    SELECT
        'dim_date_not_empty' AS check_name,
        COUNT(*) = 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Table should contain at least one row' AS check_description
    FROM marts.dim_date

    UNION ALL

    -- Check that the order fact table contains rows.
    SELECT
        'fact_orders_not_empty' AS check_name,
        COUNT(*) = 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Table should contain at least one row' AS check_description
    FROM marts.fact_orders

    UNION ALL

    -- Check that the ad spend fact table contains rows.
    SELECT
        'fact_ad_spend_not_empty' AS check_name,
        COUNT(*) = 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Table should contain at least one row' AS check_description
    FROM marts.fact_ad_spend

    UNION ALL

    -- Check that each order appears only once.
    SELECT
        'fact_orders_unique_order_id' AS check_name,
        COUNT(*) > 0 AS has_failed,
        COUNT(*) AS value_checked,
        'order_id should be unique in fact_orders' AS check_description
    FROM (
        SELECT order_id
        FROM marts.fact_orders
        GROUP BY order_id
        HAVING COUNT(*) > 1
    )

    UNION ALL

    -- Check that all orders link to a valid customer.
    SELECT
        'fact_orders_valid_customer_id' AS check_name,
        COUNT(*) > 0 AS has_failed,
        COUNT(*) AS value_checked,
        'All fact_orders.customer_id values should exist in dim_customers' AS check_description
    FROM marts.fact_orders AS orders
    LEFT JOIN marts.dim_customers AS customers
        ON orders.customer_id = customers.customer_id
    WHERE customers.customer_id IS NULL

    UNION ALL

    -- Check that all orders link to a valid product.
    SELECT
        'fact_orders_valid_product_id' AS check_name,
        COUNT(*) > 0 AS has_failed,
        COUNT(*) AS value_checked,
        'All fact_orders.product_id values should exist in dim_products' AS check_description
    FROM marts.fact_orders AS orders
    LEFT JOIN marts.dim_products AS products
        ON orders.product_id = products.product_id
    WHERE products.product_id IS NULL

    UNION ALL

    -- Check that sales values are not negative.
    SELECT
        'fact_orders_non_negative_sales_values' AS check_name,
        COUNT(*) > 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Order quantity and revenue values should not be negative' AS check_description
    FROM marts.fact_orders
    WHERE quantity < 0
       OR gross_revenue < 0
       OR net_sales_revenue < 0
       OR total_cost < 0
       OR gross_profit < 0

    UNION ALL

    -- Check that marketing values are not negative.
    SELECT
        'fact_ad_spend_non_negative_values' AS check_name,
        COUNT(*) > 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Ad spend, clicks, and impressions should not be negative' AS check_description
    FROM marts.fact_ad_spend
    WHERE spend < 0
       OR clicks < 0
       OR impressions < 0

    UNION ALL

    -- Check that refunds link to valid original orders.
    SELECT
        'fact_refunds_valid_order_id' AS check_name,
        COUNT(*) > 0 AS has_failed,
        COUNT(*) AS value_checked,
        'All fact_refunds.order_id values should exist in fact_orders' AS check_description
    FROM marts.fact_refunds AS refunds
    LEFT JOIN marts.fact_orders AS orders
        ON refunds.order_id = orders.order_id
    WHERE orders.order_id IS NULL

    UNION ALL

    -- Check that refund dates are not before order dates.
    SELECT
        'fact_refunds_valid_refund_date' AS check_name,
        COUNT(*) > 0 AS has_failed,
        COUNT(*) AS value_checked,
        'Refund date should not be before the original order date' AS check_description
    FROM marts.fact_refunds AS refunds
    LEFT JOIN marts.fact_orders AS orders
        ON refunds.order_id = orders.order_id
    WHERE refunds.refund_date < orders.order_date
)

SELECT
    check_name,
    CASE
        WHEN has_failed THEN 'FAIL'
        ELSE 'PASS'
    END AS check_status,
    value_checked,
    check_description
FROM checks
ORDER BY check_status, check_name;