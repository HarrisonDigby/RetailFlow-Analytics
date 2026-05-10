
  create or replace   view RETAILFLOW_DB.DBT_staging.stg_customers
  
  
  
  
  as (
    SELECT
    customer_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    LOWER(TRIM(email)) AS email,
    TRIM(country) AS country,
    signup_date
FROM RETAILFLOW_DB.RAW.CUSTOMERS
  );

