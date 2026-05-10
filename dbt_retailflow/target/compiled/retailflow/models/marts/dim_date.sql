WITH all_dates AS (

    SELECT order_date AS date_day
    FROM RETAILFLOW_DB.DBT_staging.stg_orders

    UNION

    SELECT spend_date AS date_day
    FROM RETAILFLOW_DB.DBT_staging.stg_ad_spend

    UNION

    SELECT refund_date AS date_day
    FROM RETAILFLOW_DB.DBT_staging.stg_refunds

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
FROM all_dates