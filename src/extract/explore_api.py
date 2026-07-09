import requests
import json
import time

url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"

def fetch_page(page_number):
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
            "Start Date", "End Date", "NAICS Code", "NAICS Description"
        ],
        "page": page_number,
        "limit": 100  # max allowed per page is usually 100
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()  # will throw an error if the request failed
    return response.json()

def fetch_all_pages(max_pages=5):
    """
    max_pages caps how many pages we pull — start small (5) to test,
    increase once you know it works.
    """
    all_results = []
    page = 1

    while page <= max_pages:
        print(f"Fetching page {page}...")
        data = fetch_page(page)
        results = data.get("results", [])
        all_results.extend(results)

        if not data["page_metadata"]["hasNext"]:
            print("No more pages.")
            break

        page += 1
        time.sleep(0.5)  # be polite to the API, avoid hammering it

    return all_results

if __name__ == "__main__":
    records = fetch_all_pages(max_pages=5)
    print(f"\nTotal records pulled: {len(records)}")

    output_path = "data/raw/dod_awards_2024.json"
    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)

    print(f"Saved to {output_path}")