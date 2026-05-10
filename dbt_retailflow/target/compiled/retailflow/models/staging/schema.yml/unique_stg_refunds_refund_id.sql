
    
    

select
    refund_id as unique_field,
    count(*) as n_records

from RETAILFLOW_DB.DBT_staging.stg_refunds
where refund_id is not null
group by refund_id
having count(*) > 1


