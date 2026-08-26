import json
import pandas as pd


# Read the raw API data
with open("data/raw/studies.json", "r", encoding="utf-8") as file:
    data = json.load(file)

records = []

# Extract selected fields from each study
for study in data["studies"]:
    protocol = study["protocolSection"]

    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {})
    design = protocol.get("designModule", {})

    record = {
        "nct_id": identification.get("nctId"),
        "brief_title": identification.get("briefTitle"),
        "overall_status": status.get("overallStatus"),
        "lead_sponsor": sponsor.get("leadSponsor", {}).get("name"),
        "enrollment": design.get("enrollmentInfo", {}).get("count"),
        "last_update_date": status.get(
            "lastUpdatePostDateStruct", {}
        ).get("date")
    }

    records.append(record)

# Convert the records into a table
studies_df = pd.DataFrame(records)

# Save the table as a CSV file
studies_df.to_csv(
    "data/processed/studies.csv",
    index=False
)

print(studies_df)
print("\nProcessed data saved to data/processed/studies.csv")