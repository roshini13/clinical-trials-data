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
# DQ003: Recruiting records should be updated within 365 days
studies_df["last_update_date"] = pd.to_datetime(
    studies_df["last_update_date"],
    errors="coerce"
)

today = pd.Timestamp.today().normalize()

studies_df["days_since_update"] = (
    today - studies_df["last_update_date"]
).dt.days

stale_studies = studies_df[
    studies_df["days_since_update"] > 365
].copy()

stale_studies.to_csv(
    "data/quality/stale_recruiting_studies.csv",
    index=False
)

if stale_studies.empty:
    print("PASS: No outdated recruiting records found.")
else:
    print(
        f"REVIEW: Found {len(stale_studies)} recruiting "
        "studies not updated within 365 days."
    )

    print(
        stale_studies[
            ["nct_id", "last_update_date", "days_since_update"]
        ]
    )
# Create a standardized operational issue table
issues_df = stale_studies[
    ["nct_id", "days_since_update"]
].copy()

issues_df["issue_id"] = (
    "DQ003-" + issues_df["nct_id"]
)

issues_df["rule_id"] = "DQ003"
issues_df["field_name"] = "last_update_date"

issues_df["issue_description"] = issues_df[
    "days_since_update"
].apply(
    lambda days: (
        f"Recruiting study has not been updated for {days} days"
    )
)

issues_df["priority"] = issues_df[
    "days_since_update"
].apply(
    lambda days: "HIGH" if days > 730 else "MEDIUM"
)

issues_df["detected_date"] = today.date().isoformat()
issues_df["issue_status"] = "OPEN"

issues_df = issues_df[
    [
        "issue_id",
        "nct_id",
        "rule_id",
        "field_name",
        "issue_description",
        "priority",
        "detected_date",
        "issue_status"
    ]
]

issues_df.to_csv(
    "data/quality/data_quality_issues.csv",
    index=False
)

print(
    f"\nCreated standardized issue table "
    f"with {len(issues_df)} open issues."
)

print(issues_df)