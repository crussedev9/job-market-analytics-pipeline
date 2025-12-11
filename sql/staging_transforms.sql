-- ============================================================================
-- Job Market Analytics Pipeline - Staging Transforms Script
-- ============================================================================
-- Purpose: Transform staging tables into the dimensional model (star schema)
--
-- Prerequisites:
--   1. Staging tables loaded (stg_dim_*, stg_fact_posting, etc.)
--   2. Target tables created (run create_tables.sql first)
--
-- Execution: Run this script after create_tables.sql
-- ============================================================================

-- ============================================================================
-- POPULATE DIMENSION TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Populate dim_job
-- ----------------------------------------------------------------------------
-- Extract unique job titles from staging and assign surrogate keys
-- TODO: Update column names to match your actual staging data
-- ----------------------------------------------------------------------------

INSERT INTO dim_job (job_id, job_title, job_category, seniority_level)
SELECT DISTINCT
    job_id,
    -- TODO: Add actual job_title column from staging
    NULL AS job_title,
    job_category,
    seniority_level
FROM stg_dim_job
WHERE job_id IS NOT NULL;

-- Verification
SELECT 'dim_job' AS table_name, COUNT(*) AS row_count FROM dim_job;


-- ----------------------------------------------------------------------------
-- Populate dim_company
-- ----------------------------------------------------------------------------
-- Extract unique companies from staging data
-- TODO: Update to match actual staging table columns
-- ----------------------------------------------------------------------------

INSERT INTO dim_company (company_id, company_name, industry, company_size)
SELECT DISTINCT
    company_id,
    company_name,
    industry,
    company_size
FROM stg_dim_company
WHERE company_id IS NOT NULL;

-- Verification
SELECT 'dim_company' AS table_name, COUNT(*) AS row_count FROM dim_company;


-- ----------------------------------------------------------------------------
-- Populate dim_location
-- ----------------------------------------------------------------------------
-- Extract unique locations with geographic hierarchy
-- TODO: Adjust column mappings as needed
-- ----------------------------------------------------------------------------

INSERT INTO dim_location (location_id, city, state, country, region, is_remote)
SELECT DISTINCT
    location_id,
    city,
    state,
    COALESCE(country, 'USA') AS country,
    region,
    COALESCE(is_remote, 0) AS is_remote
FROM stg_dim_location
WHERE location_id IS NOT NULL;

-- Verification
SELECT 'dim_location' AS table_name, COUNT(*) AS row_count FROM dim_location;


-- ----------------------------------------------------------------------------
-- Populate dim_employment_type
-- ----------------------------------------------------------------------------
-- Extract unique employment type combinations
-- ----------------------------------------------------------------------------

INSERT INTO dim_employment_type (employment_type_id, employment_type, work_arrangement)
SELECT DISTINCT
    employment_type_id,
    employment_type,
    work_arrangement
FROM stg_dim_employment_type
WHERE employment_type_id IS NOT NULL;

-- Verification
SELECT 'dim_employment_type' AS table_name, COUNT(*) AS row_count FROM dim_employment_type;


-- ----------------------------------------------------------------------------
-- Populate dim_skill
-- ----------------------------------------------------------------------------
-- Extract unique skills
-- ----------------------------------------------------------------------------

INSERT INTO dim_skill (skill_id, skill_name, skill_category)
SELECT DISTINCT
    skill_id,
    skill_name,
    skill_category
FROM stg_dim_skill
WHERE skill_id IS NOT NULL;

-- Verification
SELECT 'dim_skill' AS table_name, COUNT(*) AS row_count FROM dim_skill;


-- ============================================================================
-- POPULATE FACT TABLE
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Populate fact_posting
-- ----------------------------------------------------------------------------
-- Join staging data to get foreign keys and populate fact table
-- TODO: Adjust JOIN conditions and column names to match staging data
-- ----------------------------------------------------------------------------

INSERT INTO fact_posting (
    posting_id,
    job_id,
    company_id,
    location_id,
    employment_type_id,
    posted_date,
    salary_min,
    salary_max,
    salary_currency,
    application_url
)
SELECT
    stg.posting_id,

    -- Foreign keys (using surrogate keys from dimensions)
    -- TODO: These joins assume staging already has surrogate keys
    -- If not, you'll need to join back to dimension tables
    stg.job_id,
    stg.company_id,
    stg.location_id,
    stg.employment_type_id,

    -- Date dimension
    -- TODO: Add actual posted_date column from staging
    NULL AS posted_date,

    -- Measures
    stg.salary_min,
    stg.salary_max,
    COALESCE(stg.salary_currency, 'USD') AS salary_currency,

    -- Additional attributes
    -- TODO: Add application_url if available in staging
    NULL AS application_url

FROM stg_fact_posting stg
WHERE stg.posting_id IS NOT NULL;

-- Verification
SELECT 'fact_posting' AS table_name, COUNT(*) AS row_count FROM fact_posting;


-- ============================================================================
-- POPULATE BRIDGE TABLE
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Populate bridge_posting_skill
-- ----------------------------------------------------------------------------
-- Map job postings to required skills (many-to-many)
-- ----------------------------------------------------------------------------

INSERT INTO bridge_posting_skill (posting_id, skill_id)
SELECT DISTINCT
    posting_id,
    skill_id
FROM stg_bridge_posting_skill
WHERE posting_id IS NOT NULL
  AND skill_id IS NOT NULL;

-- Verification
SELECT 'bridge_posting_skill' AS table_name, COUNT(*) AS row_count FROM bridge_posting_skill;


-- ============================================================================
-- DATA QUALITY CHECKS
-- ============================================================================

-- Check for orphaned records in fact table (FKs that don't match dimensions)
-- ----------------------------------------------------------------------------

-- Check job_id foreign key integrity
SELECT
    'Orphaned job_id records' AS check_name,
    COUNT(*) AS orphan_count
FROM fact_posting f
LEFT JOIN dim_job j ON f.job_id = j.job_id
WHERE f.job_id IS NOT NULL
  AND j.job_id IS NULL;

-- Check company_id foreign key integrity
SELECT
    'Orphaned company_id records' AS check_name,
    COUNT(*) AS orphan_count
FROM fact_posting f
LEFT JOIN dim_company c ON f.company_id = c.company_id
WHERE f.company_id IS NOT NULL
  AND c.company_id IS NULL;

-- Check location_id foreign key integrity
SELECT
    'Orphaned location_id records' AS check_name,
    COUNT(*) AS orphan_count
FROM fact_posting f
LEFT JOIN dim_location l ON f.location_id = l.location_id
WHERE f.location_id IS NOT NULL
  AND l.location_id IS NULL;

-- TODO: Add more data quality checks:
-- - Check for NULL values in required fields
-- - Validate salary_min <= salary_max
-- - Check date ranges are reasonable
-- - Verify all skills in bridge table exist in dim_skill


-- ============================================================================
-- SUMMARY STATISTICS
-- ============================================================================

SELECT '========================================' AS summary;
SELECT 'DIMENSIONAL MODEL POPULATION COMPLETE' AS summary;
SELECT '========================================' AS summary;

-- Row counts for all tables
SELECT 'dim_job' AS table_name, COUNT(*) AS rows FROM dim_job
UNION ALL
SELECT 'dim_company', COUNT(*) FROM dim_company
UNION ALL
SELECT 'dim_location', COUNT(*) FROM dim_location
UNION ALL
SELECT 'dim_employment_type', COUNT(*) FROM dim_employment_type
UNION ALL
SELECT 'dim_skill', COUNT(*) FROM dim_skill
UNION ALL
SELECT 'fact_posting', COUNT(*) FROM fact_posting
UNION ALL
SELECT 'bridge_posting_skill', COUNT(*) FROM bridge_posting_skill;


-- ============================================================================
-- NOTES
-- ============================================================================
-- 1. This script assumes staging tables contain pre-assigned surrogate keys
--    from the Python data cleaning step.
--
-- 2. If your staging data uses natural keys, you'll need to modify the
--    INSERT statements to:
--    a) Deduplicate on natural keys
--    b) Generate surrogate keys (e.g., using ROW_NUMBER() or IDENTITY)
--    c) Join back to get surrogate keys when populating fact table
--
-- 3. For production, consider:
--    - Adding error handling and transaction management
--    - Implementing incremental loads instead of full refresh
--    - Adding audit columns (created_by, modified_date, etc.)
--
-- Next step: Run analytics_views.sql to create analytical views
-- ============================================================================
