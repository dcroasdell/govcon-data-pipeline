with date_spine as (
    select distinct cast(start_date as date) as award_date
    from {{ ref('stg_awards') }}
    where start_date is not null

    union

    select distinct cast(end_date as date) as award_date
    from {{ ref('stg_awards') }}
    where end_date is not null
)

select
    award_date,
    extract(year from award_date) as year,
    extract(quarter from award_date) as quarter,
    extract(month from award_date) as month,
    strftime(award_date, '%B') as month_name,
    row_number() over (order by award_date) as time_id

from date_spine
