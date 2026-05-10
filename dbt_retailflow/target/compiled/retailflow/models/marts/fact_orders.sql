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

FROM RETAILFLOW_DB.DBT_staging.stg_orders AS orders

LEFT JOIN RETAILFLOW_DB.DBT_staging.stg_products AS products
    ON orders.product_id = products.product_id