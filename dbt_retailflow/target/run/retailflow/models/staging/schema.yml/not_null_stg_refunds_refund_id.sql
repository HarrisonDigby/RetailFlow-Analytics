
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select refund_id
from RETAILFLOW_DB.DBT_staging.stg_refunds
where refund_id is null



  
  
      
    ) dbt_internal_test