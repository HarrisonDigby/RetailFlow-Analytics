
  create or replace   view RETAILFLOW_DB.DBT_staging.stg_ad_spend
  
  
  
  
  as (
    SELECT
    date AS spend_date,
    TRIM(platform) AS platform,
    TRIM(campaign) AS campaign,
    spend,
    clicks,
    impressions,
    cost_per_click,
    click_through_rate
FROM RETAILFLOW_DB.RAW.AD_SPEND
  );

