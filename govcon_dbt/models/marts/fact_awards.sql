select
    a.internal_id,
    a.award_id,
    v.vendor_id,
    ag.agency_id,
    t.time_id as start_time_id,
    a.award_amount,
    a.pop_state,
    a.award_description,
    a.contract_award_type,
    a.naics_code,
    a.naics_description

from {{ ref('stg_awards') }} a

left join {{ ref('dim_vendors') }} v
    on a.recipient_name = v.recipient_name

left join {{ ref('dim_agencies') }} ag
    on a.awarding_agency = ag.awarding_agency
    and a.awarding_sub_agency = ag.awarding_sub_agency

left join {{ ref('dim_time') }} t
    on cast(a.start_date as date) = t.award_date
