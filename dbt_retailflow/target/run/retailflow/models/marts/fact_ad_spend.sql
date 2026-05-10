
  
    

create or replace transient table RETAILFLOW_DB.DBT_marts.fact_ad_spend
    
    
    
    as (SELECT
    spend_date,
    platform,
    campaign,
    spend,
    clicks,
    impressions,
    cost_per_click,
    click_through_rate
FROM RETAILFLOW_DB.DBT_staging.stg_ad_spend
    )
;


  