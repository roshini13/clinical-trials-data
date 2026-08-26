import json
import requests


API_URL = "https://clinicaltrials.gov/api/v2/studies"

parameters = {
    "query.locn": "New York",
    "filter.overallStatus": "RECRUITING",
    "format": "json",
    "pageSize": 100
}

response = requests.get(API_URL, params=parameters, timeout=30)

# Stop the program if the API request was unsuccessful
response.raise_for_status()

data = response.json()
studies = data["studies"]
with open("data/raw/studies.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)

print("Raw data saved to data/raw/studies.json")
print("Main API response sections:", data.keys())
print("Sections inside one study:", studies[0].keys())
print()

print(f"Downloaded {len(studies)} studies\n")

for study in studies:
    protocol = study["protocolSection"]
    identification = protocol["identificationModule"]
    status = protocol["statusModule"]

    print("NCT ID:", identification["nctId"])
    print("Title:", identification["briefTitle"])
    print("Status:", status["overallStatus"])
    print("-" * 60)