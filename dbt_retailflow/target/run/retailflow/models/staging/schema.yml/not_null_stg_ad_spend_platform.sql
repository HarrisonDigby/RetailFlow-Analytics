
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select platform
from RETAILFLOW_DB.DBT_staging.stg_ad_spend
where platform is null



  
  
      
    ) dbt_internal_test