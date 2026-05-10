
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select product_id
from RETAILFLOW_DB.DBT_marts.fact_orders
where product_id is null



  
  
      
    ) dbt_internal_test