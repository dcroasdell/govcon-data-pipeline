with unique_vendors as (
    select distinct recipient_name
    from {{ ref('stg_awards') }}
    where recipient_name is not null
)

select
    recipient_name,
    row_number() over (order by recipient_name) as vendor_id

from unique_vendors
