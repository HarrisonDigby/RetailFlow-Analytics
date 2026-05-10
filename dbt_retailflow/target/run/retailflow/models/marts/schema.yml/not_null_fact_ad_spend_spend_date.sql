
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select spend_date
from RETAILFLOW_DB.DBT_marts.fact_ad_spend
where spend_date is null



  
  
      
    ) dbt_internal_test