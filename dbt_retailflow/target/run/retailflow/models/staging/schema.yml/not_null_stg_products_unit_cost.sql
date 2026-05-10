
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select unit_cost
from RETAILFLOW_DB.DBT_staging.stg_products
where unit_cost is null



  
  
      
    ) dbt_internal_test