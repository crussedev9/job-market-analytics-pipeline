-- ============================================================================
-- Job Market Analytics Pipeline - Create Tables Script
-- ============================================================================
-- Purpose: Create the dimensional model (star schema) tables
--
-- Schema: 1 Fact Table + 5 Dimension Tables + 1 Bridge Table
--
-- Execution: Run this script in SQLite after loading staging tables
-- ============================================================================

-- Drop existing tables if they exist (for clean re-runs)
DROP TABLE IF EXISTS bridge_posting_skill;
DROP TABLE IF EXISTS fact_posting;
DROP TABLE IF EXISTS dim_skill;
DROP TABLE IF EXISTS dim_employment_type;
DROP TABLE IF EXISTS dim_location;
DROP TABLE IF EXISTS dim_company;
DROP TABLE IF EXISTS dim_job;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- dim_job: Job title dimension
-- ----------------------------------------------------------------------------
-- Purpose: Store unique job titles with categorization and seniority
-- Grain: One row per unique job title
-- ----------------------------------------------------------------------------
CREATE TABLE dim_job (
    job_id INTEGER PRIMARY KEY,
    job_title VARCHAR(255),
    job_category VARCHAR(100),           -- e.g., 'Data Analytics', 'Data Science', 'BI'
    seniority_level VARCHAR(50),         -- e.g., 'Junior', 'Mid-level', 'Senior', 'Lead'
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TODO: Add indexes on commonly filtered columns
-- CREATE INDEX idx_dim_job_category ON dim_job(job_category);
-- CREATE INDEX idx_dim_job_seniority ON dim_job(seniority_level);


-- ----------------------------------------------------------------------------
-- dim_company: Company dimension
-- ----------------------------------------------------------------------------
-- Purpose: Store unique companies posting jobs
-- Grain: One row per company
-- ----------------------------------------------------------------------------
CREATE TABLE dim_company (
    company_id INTEGER PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),               -- e.g., 'Technology', 'Finance', 'Healthcare'
    company_size VARCHAR(50),            -- e.g., '1-50', '51-200', '201-1000', '1000+'
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TODO: Add unique constraint on company_name if needed
-- CREATE UNIQUE INDEX idx_dim_company_name ON dim_company(company_name);


-- ----------------------------------------------------------------------------
-- dim_location: Geographic dimension
-- ----------------------------------------------------------------------------
-- Purpose: Store unique locations with geographic hierarchy
-- Grain: One row per unique location
-- ----------------------------------------------------------------------------
CREATE TABLE dim_location (
    location_id INTEGER PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100) DEFAULT 'USA',
    region VARCHAR(50),                  -- e.g., 'Northeast', 'West Coast', 'Midwest'
    is_remote BOOLEAN DEFAULT 0,         -- 1 if location is remote, 0 otherwise
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TODO: Add indexes for geographic filtering
-- CREATE INDEX idx_dim_location_state ON dim_location(state);
-- CREATE INDEX idx_dim_location_remote ON dim_location(is_remote);


-- ----------------------------------------------------------------------------
-- dim_employment_type: Employment and work arrangement dimension
-- ----------------------------------------------------------------------------
-- Purpose: Store employment types and work arrangements
-- Grain: One row per unique employment type + work arrangement combination
-- ----------------------------------------------------------------------------
CREATE TABLE dim_employment_type (
    employment_type_id INTEGER PRIMARY KEY,
    employment_type VARCHAR(50),         -- e.g., 'Full-time', 'Contract', 'Part-time'
    work_arrangement VARCHAR(50),        -- e.g., 'Remote', 'Hybrid', 'On-site'
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ----------------------------------------------------------------------------
-- dim_skill: Skills dimension
-- ----------------------------------------------------------------------------
-- Purpose: Store unique skills required across job postings
-- Grain: One row per unique skill
-- ----------------------------------------------------------------------------
CREATE TABLE dim_skill (
    skill_id INTEGER PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(100),         -- e.g., 'Programming', 'BI Tools', 'Cloud', 'Databases'
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TODO: Add unique constraint on skill_name
-- CREATE UNIQUE INDEX idx_dim_skill_name ON dim_skill(skill_name);


-- ============================================================================
-- FACT TABLE
-- ============================================================================

-- ----------------------------------------------------------------------------
-- fact_posting: Job posting fact table
-- ----------------------------------------------------------------------------
-- Purpose: Store facts about each job posting
-- Grain: One row per job posting
-- ----------------------------------------------------------------------------
CREATE TABLE fact_posting (
    posting_id INTEGER PRIMARY KEY,

    -- Foreign keys to dimensions
    job_id INTEGER,
    company_id INTEGER,
    location_id INTEGER,
    employment_type_id INTEGER,

    -- Date dimension (simplified - using single date field)
    posted_date DATE,

    -- Measures
    salary_min DECIMAL(10, 2),           -- Minimum salary
    salary_max DECIMAL(10, 2),           -- Maximum salary
    salary_currency VARCHAR(10) DEFAULT 'USD',

    -- Additional attributes
    application_url VARCHAR(500),

    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key constraints
    FOREIGN KEY (job_id) REFERENCES dim_job(job_id),
    FOREIGN KEY (company_id) REFERENCES dim_company(company_id),
    FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (employment_type_id) REFERENCES dim_employment_type(employment_type_id)
);

-- TODO: Add indexes on foreign keys for query performance
-- CREATE INDEX idx_fact_posting_job ON fact_posting(job_id);
-- CREATE INDEX idx_fact_posting_company ON fact_posting(company_id);
-- CREATE INDEX idx_fact_posting_location ON fact_posting(location_id);
-- CREATE INDEX idx_fact_posting_employment ON fact_posting(employment_type_id);
-- CREATE INDEX idx_fact_posting_date ON fact_posting(posted_date);


-- ============================================================================
-- BRIDGE TABLE (Many-to-Many Relationship)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- bridge_posting_skill: Job posting to skills mapping
-- ----------------------------------------------------------------------------
-- Purpose: Handle many-to-many relationship between postings and skills
-- Grain: One row per posting-skill combination
-- Note: A single posting can require multiple skills
-- ----------------------------------------------------------------------------
CREATE TABLE bridge_posting_skill (
    posting_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,

    -- Metadata
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Composite primary key
    PRIMARY KEY (posting_id, skill_id),

    -- Foreign key constraints
    FOREIGN KEY (posting_id) REFERENCES fact_posting(posting_id),
    FOREIGN KEY (skill_id) REFERENCES dim_skill(skill_id)
);

-- TODO: Add indexes for reverse lookups
-- CREATE INDEX idx_bridge_skill ON bridge_posting_skill(skill_id);


-- ============================================================================
-- SUMMARY
-- ============================================================================
-- Tables created:
-- 1. dim_job              (Job titles and categories)
-- 2. dim_company          (Companies)
-- 3. dim_location         (Geographic locations)
-- 4. dim_employment_type  (Employment types and work arrangements)
-- 5. dim_skill            (Technical skills)
-- 6. fact_posting         (Job postings - fact table)
-- 7. bridge_posting_skill (Posting-skill mappings)
--
-- Next step: Run staging_transforms.sql to populate these tables
-- ============================================================================
