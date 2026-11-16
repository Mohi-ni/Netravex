CREATE TABLE scoping_inquiries (
    id SERIAL PRIMARY KEY,
    reference_id VARCHAR(20) UNIQUE NOT NULL, -- e.g., NVX-84920
    full_name VARCHAR(120) NOT NULL,
    organization_name VARCHAR(150) NOT NULL,
    org_type VARCHAR(50) DEFAULT 'Co-operative Bank',
    work_email VARCHAR(150) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    readiness_score INT DEFAULT 0, -- Out of 10 from the scorecard
    checked_items JSONB,           -- Stores which of the 10 items they checked
    consent_given BOOLEAN NOT NULL DEFAULT TRUE,
    consent_timestamp TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(30) DEFAULT 'NEW',
    created_at TIMESTAMPTZ DEFAULT NOW()
);