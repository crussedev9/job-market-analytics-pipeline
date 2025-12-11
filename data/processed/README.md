# Processed Data Folder

This folder contains final, analytics-ready tables exported from the SQL dimensional model.

## Purpose

The processed folder holds the final output of the ETL pipeline - clean, structured data ready for consumption by Power BI or other BI tools.

## Contents

These files are created after running the SQL transformations:

### Dimensional Model Tables:
- `fact_posting.csv` - Fact table with one row per job posting
- `dim_job.csv` - Job dimension (titles, categories, seniority)
- `dim_company.csv` - Company dimension
- `dim_location.csv` - Location dimension with geographic hierarchy
- `dim_employment_type.csv` - Employment type and work arrangement dimension
- `dim_skill.csv` - Skills dimension
- `bridge_posting_skill.csv` - Bridge table for posting-skill many-to-many relationship

### Analytical Views (Optional):
- `vw_salary_by_title_and_location.csv` - Pre-aggregated salary analysis
- `vw_skill_demand.csv` - Skills ranked by demand
- `vw_remote_vs_onsite_trends.csv` - Work arrangement trends over time
- `vw_job_posting_details.csv` - Denormalized view with all dimensions joined

## Data Quality

All files in this folder have:
- Consistent column naming (lowercase snake_case)
- Proper data types
- No duplicate records (except where intentional in bridge tables)
- Referential integrity maintained between fact and dimension tables

## Usage

### Option 1: Power BI Connection to SQLite
Connect Power BI directly to the `job_market.db` SQLite database and query the tables/views.

### Option 2: Power BI Connection to CSV Files
Import these CSV files into Power BI and establish relationships based on the dimensional model.

Recommended approach: Use the Power Query M code provided in `power_query/job_postings_power_query_m_code.txt` to load and shape this data.

## Important Notes

- These files represent the **final output** of the data pipeline
- They are **not tracked in Git** (see `.gitignore`)
- Regenerate these files by running the complete ETL pipeline end-to-end
- These files are optimized for analytical queries, not transactional operations

## Relationships

```
fact_posting
├── job_id → dim_job.job_id
├── company_id → dim_company.company_id
├── location_id → dim_location.location_id
└── employment_type_id → dim_employment_type.employment_type_id

bridge_posting_skill
├── posting_id → fact_posting.posting_id
└── skill_id → dim_skill.skill_id
```

## Refresh Schedule

For a production implementation, these files would be refreshed:
- Daily for new job postings
- Weekly for full historical refresh
- On-demand when source data changes

For this demo project, regenerate by running the Python and SQL scripts.
