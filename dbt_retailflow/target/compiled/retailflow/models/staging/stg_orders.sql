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
        ELSE 0
    END AS net_sales_revenue
FROM RETAILFLOW_DB.RAW.ORDERS