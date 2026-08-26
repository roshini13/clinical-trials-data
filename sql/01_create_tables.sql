CREATE TABLE IF NOT EXISTS clinical_studies (
    nct_id VARCHAR(11) PRIMARY KEY,
    brief_title TEXT NOT NULL,
    overall_status VARCHAR(50) NOT NULL,
    lead_sponsor TEXT,
    enrollment INTEGER CHECK (enrollment >= 0),
    last_update_date DATE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_quality_issues (
    issue_id VARCHAR(50) PRIMARY KEY,
    nct_id VARCHAR(11) NOT NULL,
    rule_id VARCHAR(10) NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    issue_description TEXT NOT NULL,
    priority VARCHAR(10) NOT NULL
        CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
    detected_date DATE NOT NULL,
    issue_status VARCHAR(20) NOT NULL
        CHECK (
            issue_status IN ('OPEN', 'IN_PROGRESS', 'RESOLVED')
        ),
    assigned_to VARCHAR(150),
    resolved_date DATE,
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_issue_study
        FOREIGN KEY (nct_id)
        REFERENCES clinical_studies(nct_id)
);

CREATE INDEX IF NOT EXISTS idx_issue_status
    ON data_quality_issues(issue_status);

CREATE INDEX IF NOT EXISTS idx_issue_priority
    ON data_quality_issues(priority);