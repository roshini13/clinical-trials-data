CREATE OR REPLACE VIEW vw_quality_overview AS
WITH study_metrics AS (
    SELECT
        COUNT(*) AS total_studies,
        COALESCE(SUM(enrollment), 0) AS total_enrollment
    FROM clinical_studies
),
issue_metrics AS (
    SELECT
        COUNT(*) FILTER (
            WHERE issue_status = 'OPEN'
        ) AS open_issues,

        COUNT(*) FILTER (
            WHERE issue_status = 'OPEN'
              AND priority = 'HIGH'
        ) AS high_priority_issues,

        COUNT(DISTINCT nct_id) FILTER (
            WHERE issue_status = 'OPEN'
        ) AS studies_with_open_issues
    FROM data_quality_issues
)
SELECT
    study_metrics.total_studies,
    study_metrics.total_enrollment,
    issue_metrics.open_issues,
    issue_metrics.high_priority_issues,
    issue_metrics.studies_with_open_issues,

    ROUND(
        100.0 * issue_metrics.studies_with_open_issues
        / NULLIF(study_metrics.total_studies, 0),
        2
    ) AS affected_study_percentage
FROM study_metrics
CROSS JOIN issue_metrics;


CREATE OR REPLACE VIEW vw_issues_by_priority AS
SELECT
    priority,
    issue_status,
    COUNT(*) AS issue_count,
    COUNT(DISTINCT nct_id) AS affected_studies
FROM data_quality_issues
GROUP BY
    priority,
    issue_status;


CREATE OR REPLACE VIEW vw_study_issue_details AS
SELECT
    studies.nct_id,
    studies.brief_title,
    studies.lead_sponsor,
    studies.enrollment,
    studies.last_update_date,
    issues.issue_id,
    issues.rule_id,
    issues.issue_description,
    issues.priority,
    issues.detected_date,
    issues.issue_status,
    CURRENT_DATE - studies.last_update_date
        AS days_since_update
FROM clinical_studies AS studies
INNER JOIN data_quality_issues AS issues
    ON studies.nct_id = issues.nct_id;


CREATE OR REPLACE VIEW vw_sponsor_summary AS
WITH issue_counts AS (
    SELECT
        nct_id,
        COUNT(*) FILTER (
            WHERE issue_status = 'OPEN'
        ) AS open_issue_count,

        COUNT(*) FILTER (
            WHERE issue_status = 'OPEN'
              AND priority = 'HIGH'
        ) AS high_priority_count
    FROM data_quality_issues
    GROUP BY nct_id
)
SELECT
    studies.lead_sponsor,
    COUNT(*) AS study_count,
    COALESCE(SUM(studies.enrollment), 0)
        AS total_planned_enrollment,
    COALESCE(SUM(issue_counts.open_issue_count), 0)
        AS open_issue_count,
    COALESCE(SUM(issue_counts.high_priority_count), 0)
        AS high_priority_count
FROM clinical_studies AS studies
LEFT JOIN issue_counts
    ON studies.nct_id = issue_counts.nct_id
GROUP BY studies.lead_sponsor;