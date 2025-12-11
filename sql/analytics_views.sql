-- ============================================================================
-- Job Market Analytics Pipeline - Analytics Views Script
-- ============================================================================
-- Purpose: Create analytical views that answer key business questions
--
-- These views are optimized for Power BI consumption and provide
-- pre-aggregated or denormalized data for common analytical queries.
--
-- Prerequisites:
--   1. Dimensional model populated (run staging_transforms.sql first)
--
-- Execution: Run this script after staging_transforms.sql
-- ============================================================================

-- Drop existing views if they exist
DROP VIEW IF EXISTS vw_job_posting_details;
DROP VIEW IF EXISTS vw_salary_by_title_and_location;
DROP VIEW IF EXISTS vw_skill_demand;
DROP VIEW IF EXISTS vw_remote_vs_onsite_trends;


-- ============================================================================
-- VIEW 1: Job Posting Details (Denormalized)
-- ============================================================================
-- Purpose: Fully denormalized view with all dimensions joined
-- Use case: Ad-hoc analysis, drill-through details, searchable table
-- ============================================================================

CREATE VIEW vw_job_posting_details AS
SELECT
    -- Fact table identifiers
    f.posting_id,
    f.posted_date,

    -- Job dimension
    j.job_title,
    j.job_category,
    j.seniority_level,

    -- Company dimension
    c.company_name,
    c.industry,
    c.company_size,

    -- Location dimension
    l.city,
    l.state,
    l.country,
    l.region,
    l.is_remote,

    -- Employment type dimension
    e.employment_type,
    e.work_arrangement,

    -- Salary measures
    f.salary_min,
    f.salary_max,
    f.salary_currency,

    -- Calculated fields
    CASE
        WHEN f.salary_min IS NOT NULL AND f.salary_max IS NOT NULL
        THEN (f.salary_min + f.salary_max) / 2.0
        ELSE NULL
    END AS salary_midpoint,

    -- Additional attributes
    f.application_url,

    -- Skill aggregation (count of skills for this posting)
    (SELECT COUNT(*)
     FROM bridge_posting_skill bps
     WHERE bps.posting_id = f.posting_id) AS skill_count

FROM fact_posting f
LEFT JOIN dim_job j ON f.job_id = j.job_id
LEFT JOIN dim_company c ON f.company_id = c.company_id
LEFT JOIN dim_location l ON f.location_id = l.location_id
LEFT JOIN dim_employment_type e ON f.employment_type_id = e.employment_type_id;

-- TODO: Add filters for data quality (e.g., WHERE posted_date IS NOT NULL)


-- ============================================================================
-- VIEW 2: Salary Analysis by Title and Location
-- ============================================================================
-- Purpose: Aggregate salary statistics by job title and location
-- Use case: Compensation analysis, salary benchmarking
-- Business question: "How do salaries vary by job title and location?"
-- ============================================================================

CREATE VIEW vw_salary_by_title_and_location AS
SELECT
    -- Grouping dimensions
    j.job_title,
    j.job_category,
    j.seniority_level,
    l.city,
    l.state,
    l.region,
    l.is_remote,

    -- Aggregated measures
    COUNT(f.posting_id) AS posting_count,

    -- Salary statistics
    ROUND(AVG(f.salary_min), 2) AS avg_salary_min,
    ROUND(AVG(f.salary_max), 2) AS avg_salary_max,
    ROUND(AVG((f.salary_min + f.salary_max) / 2.0), 2) AS avg_salary_midpoint,

    MIN(f.salary_min) AS min_salary,
    MAX(f.salary_max) AS max_salary,

    -- Percentiles would require window functions or subqueries (TODO)
    -- TODO: Add 25th, 50th (median), 75th percentile salary calculations

    -- Data quality indicator
    ROUND(
        COUNT(CASE WHEN f.salary_min IS NOT NULL AND f.salary_max IS NOT NULL THEN 1 END) * 100.0 / COUNT(*),
        2
    ) AS pct_with_salary_data

FROM fact_posting f
LEFT JOIN dim_job j ON f.job_id = j.job_id
LEFT JOIN dim_location l ON f.location_id = l.location_id

-- Filter for records with meaningful location (optional)
-- WHERE l.city IS NOT NULL OR l.is_remote = 1

GROUP BY
    j.job_title,
    j.job_category,
    j.seniority_level,
    l.city,
    l.state,
    l.region,
    l.is_remote

HAVING COUNT(f.posting_id) >= 1;  -- TODO: Adjust threshold (e.g., >= 5 for statistical significance)


-- ============================================================================
-- VIEW 3: Skill Demand Analysis
-- ============================================================================
-- Purpose: Rank skills by demand (number of job postings requiring them)
-- Use case: Skills gap analysis, learning path planning
-- Business question: "Which skills are most in demand for analytics roles?"
-- ============================================================================

CREATE VIEW vw_skill_demand AS
SELECT
    -- Skill information
    s.skill_name,
    s.skill_category,

    -- Demand metrics
    COUNT(DISTINCT bps.posting_id) AS posting_count,

    -- Percentage of total postings requiring this skill
    ROUND(
        COUNT(DISTINCT bps.posting_id) * 100.0 / (SELECT COUNT(*) FROM fact_posting),
        2
    ) AS pct_of_total_postings,

    -- Average salary for jobs requiring this skill
    ROUND(AVG((f.salary_min + f.salary_max) / 2.0), 2) AS avg_salary_for_skill,

    -- TODO: Add trend analysis (posting count change over time)
    -- TODO: Add skill co-occurrence analysis (which skills appear together)

    -- Breakdown by job category
    -- (Requires aggregation; simplified here)
    COUNT(DISTINCT CASE WHEN j.job_category = 'Data Analytics' THEN bps.posting_id END) AS analytics_postings,
    COUNT(DISTINCT CASE WHEN j.job_category = 'Data Science' THEN bps.posting_id END) AS data_science_postings,
    COUNT(DISTINCT CASE WHEN j.job_category = 'Data Engineering' THEN bps.posting_id END) AS data_engineering_postings

FROM dim_skill s
INNER JOIN bridge_posting_skill bps ON s.skill_id = bps.skill_id
INNER JOIN fact_posting f ON bps.posting_id = f.posting_id
LEFT JOIN dim_job j ON f.job_id = j.job_id

GROUP BY
    s.skill_name,
    s.skill_category

ORDER BY posting_count DESC;


-- ============================================================================
-- VIEW 4: Remote vs On-Site Trends
-- ============================================================================
-- Purpose: Analyze distribution of work arrangements over time
-- Use case: Remote work trend analysis
-- Business question: "What is the trend for remote vs on-site roles?"
-- ============================================================================

CREATE VIEW vw_remote_vs_onsite_trends AS
SELECT
    -- Time dimension
    -- TODO: Extract year-month from posted_date for time series
    -- STRFTIME('%Y-%m', f.posted_date) AS posting_month,
    -- For now, grouping by work arrangement only
    e.work_arrangement,

    -- Breakdowns
    j.job_category,
    j.seniority_level,

    -- Aggregated measures
    COUNT(f.posting_id) AS posting_count,

    -- Percentage calculation
    ROUND(
        COUNT(f.posting_id) * 100.0 /
        SUM(COUNT(f.posting_id)) OVER (PARTITION BY j.job_category),
        2
    ) AS pct_within_category,

    -- Salary comparison by work arrangement
    ROUND(AVG((f.salary_min + f.salary_max) / 2.0), 2) AS avg_salary,

    -- Location diversity (count of unique locations)
    COUNT(DISTINCT f.location_id) AS unique_locations

FROM fact_posting f
LEFT JOIN dim_employment_type e ON f.employment_type_id = e.employment_type_id
LEFT JOIN dim_job j ON f.job_id = j.job_id

GROUP BY
    -- posting_month,  -- TODO: Uncomment when date parsing is added
    e.work_arrangement,
    j.job_category,
    j.seniority_level

ORDER BY
    -- posting_month DESC,  -- TODO: Uncomment for time series
    posting_count DESC;


-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================
-- Run these to verify views were created successfully
-- ============================================================================

-- Check view creation
SELECT
    name AS view_name,
    'Created' AS status
FROM sqlite_master
WHERE type = 'view'
  AND name LIKE 'vw_%'
ORDER BY name;

-- Sample data from each view
-- ----------------------------------------------------------------------------

-- Sample: Job Posting Details
SELECT 'vw_job_posting_details' AS view_name, COUNT(*) AS row_count
FROM vw_job_posting_details;

-- SELECT * FROM vw_job_posting_details LIMIT 5;


-- Sample: Salary by Title and Location
SELECT 'vw_salary_by_title_and_location' AS view_name, COUNT(*) AS row_count
FROM vw_salary_by_title_and_location;

-- SELECT * FROM vw_salary_by_title_and_location LIMIT 5;


-- Sample: Skill Demand
SELECT 'vw_skill_demand' AS view_name, COUNT(*) AS row_count
FROM vw_skill_demand;

-- SELECT * FROM vw_skill_demand LIMIT 10;


-- Sample: Remote vs On-site Trends
SELECT 'vw_remote_vs_onsite_trends' AS view_name, COUNT(*) AS row_count
FROM vw_remote_vs_onsite_trends;

-- SELECT * FROM vw_remote_vs_onsite_trends LIMIT 5;


-- ============================================================================
-- NOTES FOR POWER BI INTEGRATION
-- ============================================================================
-- 1. Import these views directly into Power BI for instant analytics
--
-- 2. Recommended visualizations:
--    - vw_job_posting_details: Table visual, drill-through page
--    - vw_salary_by_title_and_location: Box plot, map, bar chart
--    - vw_skill_demand: Horizontal bar chart (top 20 skills)
--    - vw_remote_vs_onsite_trends: Line chart (time series), donut chart
--
-- 3. For better performance in Power BI:
--    - Consider materialized views (not supported in SQLite, but in other DBs)
--    - Add indexes on frequently filtered columns in base tables
--    - Use DirectQuery mode for real-time data, Import mode for performance
--
-- 4. TODO: Additional views to consider:
--    - Company hiring activity (top companies by posting count)
--    - Geographic concentration (job density by metro area)
--    - Salary bands by seniority level
--    - Skills co-occurrence matrix (which skills appear together)
--
-- Next step: Connect Power BI using Power Query M code from power_query/ folder
-- ============================================================================
