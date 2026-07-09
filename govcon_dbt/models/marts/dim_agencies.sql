with unique_agencies as (
    select distinct
        awarding_agency,
        awarding_sub_agency
    from {{ ref('stg_awards') }}
    where awarding_agency is not null
)

select
    awarding_agency,
    awarding_sub_agency,
    row_number() over (order by awarding_agency, awarding_sub_agency) as agency_id

from unique_agencies
