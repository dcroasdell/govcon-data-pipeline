select
    internal_id,
    "Award ID" as award_id,
    "Recipient Name" as recipient_name,
    "Award Amount" as award_amount,
    "Awarding Agency" as awarding_agency,
    "Awarding Sub Agency" as awarding_sub_agency,
    "Start Date" as start_date,
    "End Date" as end_date,
    "NAICS Code" as naics_code,
    "NAICS Description" as naics_description,
    agency_slug,
    generated_internal_id

from raw_awards