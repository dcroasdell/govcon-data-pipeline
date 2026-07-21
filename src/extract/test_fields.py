import requests
import json

url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"

payload = {
    "filters": {
        "award_type_codes": ["A", "B", "C", "D"],
        "agencies": [
            {
                "type": "awarding",
                "tier": "toptier",
                "name": "Department of Defense"
            }
        ],
        "time_period": [
            {"start_date": "2024-01-01", "end_date": "2024-12-31"}
        ]
    },
    "fields": [
        "Award ID", "Recipient Name", "Award Amount",
        "Awarding Agency", "Awarding Sub Agency",
        "Funding Agency", "Funding Sub Agency",
        "Place of Performance State Code", "Place of Performance City",
        "Recipient Location State Code", "Recipient Location City",
        "Description",
        "Contract Award Type",
        "Start Date", "End Date"
    ],
    "page": 1,
    "limit": 5
}

response = requests.post(url, json=payload)

if response.status_code != 200:
    print(f"ERROR {response.status_code}:")
    print(response.text)
else:
    data = response.json()
    print(json.dumps(data.get("results", []), indent=2))