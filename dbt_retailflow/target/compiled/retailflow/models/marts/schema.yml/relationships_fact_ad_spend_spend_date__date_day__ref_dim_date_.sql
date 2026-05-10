
    
    

with child as (
    select spend_date as from_field
    from RETAILFLOW_DB.DBT_marts.fact_ad_spend
    where spend_date is not null
),

parent as (
    select date_day as to_field
    from RETAILFLOW_DB.DBT_marts.dim_date
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


