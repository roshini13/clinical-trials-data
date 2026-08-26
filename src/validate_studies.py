import pandas as pd


# Read the processed study-level table
studies_df = pd.read_csv("data/processed/studies.csv")

required_fields = [
    "nct_id",
    "brief_title",
    "overall_status",
    "lead_sponsor",
    "enrollment",
    "last_update_date"
]

# Count missing values in each required field
missing_counts = studies_df[required_fields].isna().sum()

# Convert the results into a report table
quality_report = (
    missing_counts
    .rename_axis("field_name")
    .reset_index(name="missing_count")
)

quality_report["rule_id"] = "DQ001"
quality_report["rule_description"] = "Required field must not be missing"

quality_report.to_csv(
    "data/quality/missing_values_report.csv",
    index=False
)

print(quality_report)

total_missing = quality_report["missing_count"].sum()

if total_missing == 0:
    print("\nPASS: No required values are missing.")
else:
    print(f"\nFAIL: Found {total_missing} missing required values.")
    # DQ002: NCT IDs must be unique
duplicate_studies = studies_df[
    studies_df.duplicated(
        subset=["nct_id"],
        keep=False
    )
].copy()

duplicate_studies.to_csv(
    "data/quality/duplicate_nct_ids.csv",
    index=False
)

if duplicate_studies.empty:
    print("PASS: No duplicate NCT IDs found.")
else:
    print(
        f"FAIL: Found {len(duplicate_studies)} "
        "records with duplicate NCT IDs."
    )