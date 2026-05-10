SELECT
    refunds.refund_id,
    refunds.order_id,
    orders.customer_id,
    orders.product_id,
    refunds.refund_date,
    refunds.refund_reason,
    orders.gross_revenue AS refund_order_value

FROM RETAILFLOW_DB.DBT_staging.stg_refunds AS refunds

LEFT JOIN RETAILFLOW_DB.DBT_staging.stg_orders AS orders
    ON refunds.order_id = orders.order_id