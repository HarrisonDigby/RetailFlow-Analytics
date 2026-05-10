SELECT
    product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    unit_price,
    unit_cost,
    unit_margin,
    ROUND(unit_margin / NULLIF(unit_price, 0), 4) AS margin_rate
FROM RETAILFLOW_DB.RAW.PRODUCTS