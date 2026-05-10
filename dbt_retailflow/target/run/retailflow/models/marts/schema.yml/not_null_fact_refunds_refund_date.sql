
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select refund_date
from RETAILFLOW_DB.DBT_marts.fact_refunds
where refund_date is null



  
  
      
    ) dbt_internal_test