
  
    

create or replace transient table RETAILFLOW_DB.DBT_marts.dim_customers
    
    
    
    as (SELECT
    customer_id,
    first_name,
    last_name,
    email,
    country,
    signup_date
FROM RETAILFLOW_DB.DBT_staging.stg_customers
    )
;


  