
  create or replace   view RETAILFLOW_DB.DBT_staging.stg_refunds
  
  
  
  
  as (
    SELECT
    refund_id,
    order_id,
    refund_date,
    TRIM(refund_reason) AS refund_reason
FROM RETAILFLOW_DB.RAW.REFUNDS
  );

