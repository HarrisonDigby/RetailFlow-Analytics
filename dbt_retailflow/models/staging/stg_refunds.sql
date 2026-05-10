SELECT
    refund_id,
    order_id,
    refund_date,
    TRIM(refund_reason) AS refund_reason
FROM {{ source('raw', 'REFUNDS') }}