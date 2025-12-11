# Pipeline Design Documentation

## Overview

The Job Market Analytics Pipeline is an end-to-end ETL (Extract, Transform, Load) system that processes raw job posting data through multiple stages to produce analytics-ready dimensional models for Business Intelligence dashboards.

**Pipeline Type:** Batch ETL (full refresh)

**Orchestration:** Manual execution (future: Airflow or cron)

**Data Flow:** CSV → Python → SQLite → SQL Transformations → Power Query → Power BI

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  Kaggle Job Postings CSV                                                │
│  (job_postings_raw.csv)                                                 │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   STAGE 1: INGESTION (Python)                           │
├─────────────────────────────────────────────────────────────────────────┤
│  Script: 01_ingest_raw_files.py                                         │
│  Actions:                                                               │
│   - Read raw CSV with pandas                                            │
│   - Validate file existence and basic schema                            │
│   - Display summary statistics                                          │
│   - Output: data/interim/job_postings_raw_combined.csv                  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│             STAGE 2: CLEANING & NORMALIZATION (Python)                  │
├─────────────────────────────────────────────────────────────────────────┤
│  Script: 02_clean_and_normalize.py                                      │
│  Actions:                                                               │
│   - Normalize column names (snake_case)                                 │
│   - Parse salary ranges → salary_min, salary_max                        │
│   - Standardize locations → city, state, country, is_remote             │
│   - Derive seniority level from job title                               │
│   - Categorize jobs (Analytics, Data Science, BI, etc.)                 │
│   - Extract skills from descriptions                                    │
│   - Create dimension tables (deduplication + surrogate keys)            │
│   - Create fact table base                                              │
│   - Create bridge table (posting-skill mappings)                        │
│  Outputs: (to data/interim/)                                            │
│   - job_postings_cleaned.csv                                            │
│   - dim_job.csv, dim_company.csv, dim_location.csv                      │
│   - dim_employment_type.csv, dim_skill.csv                              │
│   - bridge_posting_skill.csv                                            │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               STAGE 3: DATABASE LOAD (Python + SQLite)                  │
├─────────────────────────────────────────────────────────────────────────┤
│  Script: 03_export_for_sql_load.py                                      │
│  Actions:                                                               │
│   - Create SQLite connection (job_market.db)                            │
│   - Load all interim CSVs into staging tables:                          │
│       • stg_dim_job, stg_dim_company, stg_dim_location                  │
│       • stg_dim_employment_type, stg_dim_skill                          │
│       • stg_fact_posting, stg_bridge_posting_skill                      │
│   - Display database summary                                            │
│  Output: job_market.db (SQLite database)                                │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│          STAGE 4: DIMENSIONAL MODEL CREATION (SQL)                      │
├─────────────────────────────────────────────────────────────────────────┤
│  Script: sql/create_tables.sql                                          │
│  Actions:                                                               │
│   - DROP existing tables (if any)                                       │
│   - CREATE dimensional model tables:                                    │
│       • fact_posting (with foreign keys)                                │
│       • dim_job, dim_company, dim_location                              │
│       • dim_employment_type, dim_skill                                  │
│       • bridge_posting_skill                                            │
│   - Define primary keys, foreign keys, constraints                      │
│  Output: Empty dimensional tables in job_market.db                      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│         STAGE 5: DATA TRANSFORMATION (SQL)                              │
├─────────────────────────────────────────────────────────────────────────┤
│  Script: sql/staging_transforms.sql                                     │
│  Actions:                                                               │
│   - INSERT INTO dimensions from staging tables                          │
│   - INSERT INTO fact_posting (joining to get FKs)                       │
│   - INSERT INTO bridge_posting_skill                                    │
│   - Run data quality checks (orphaned records, nulls)                   │
│   - Display summary statistics                                          │
│  Output: Populated dimensional model                                    │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            STAGE 6: ANALYTICAL VIEWS (SQL)                              │
├─────────────────────────────────────────────────────────────────────────┤
│  Script: sql/analytics_views.sql                                        │
│  Actions:                                                               │
│   - CREATE VIEW vw_job_posting_details (denormalized)                   │
│   - CREATE VIEW vw_salary_by_title_and_location                         │
│   - CREATE VIEW vw_skill_demand                                         │
│   - CREATE VIEW vw_remote_vs_onsite_trends                              │
│  Output: Analytical views optimized for Power BI                        │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│         STAGE 7: POWER QUERY TRANSFORMATION (M Language)                │
├─────────────────────────────────────────────────────────────────────────┤
│  Script: power_query/job_postings_power_query_m_code.txt                │
│  Actions:                                                               │
│   - Connect to SQLite views OR processed CSV files                      │
│   - Apply final transformations:                                        │
│       • Date filtering (e.g., last 12 months)                           │
│       • Derived columns (salary_midpoint, salary_band)                  │
│       • Data type enforcement                                           │
│       • Column renaming for dashboard readability                       │
│  Output: Power Query tables ready for Power BI import                   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                STAGE 8: VISUALIZATION (Power BI)                        │
├─────────────────────────────────────────────────────────────────────────┤
│  Tool: Power BI Desktop                                                 │
│  Actions:                                                               │
│   - Import data from Power Query                                        │
│   - Create relationships (if using CSV import)                          │
│   - Define DAX measures (Avg Salary, % Remote, etc.)                    │
│   - Build dashboard pages (Overview, Skills, Salary, etc.)              │
│   - Add slicers, filters, drill-through                                 │
│  Output: Job_Market_Analytics_Dashboard.pbix                            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Pipeline Stages (Detailed)

### Stage 1: Ingestion

**Objective:** Read raw CSV and validate basic structure

**Technology:** Python (pandas)

**Input:** `data/raw/job_postings_raw.csv`

**Process:**
1. Check file existence and readability
2. Load CSV with pandas (handle encoding issues)
3. Display basic info: row count, columns, data types, null counts
4. Validate expected columns exist (job_id, title, company, location, etc.)
5. Output combined raw file for next stage

**Output:** `data/interim/job_postings_raw_combined.csv`

**Error Handling:**
- File not found → Exit with clear error message
- Encoding issues → Try multiple encodings (utf-8, latin1)
- Schema mismatch → Warn but continue

---

### Stage 2: Cleaning & Normalization

**Objective:** Clean data and prepare dimensional model components

**Technology:** Python (pandas, numpy)

**Input:** `data/interim/job_postings_raw_combined.csv`

**Process:**

1. **Column Normalization**
   - Convert to lowercase snake_case
   - Remove special characters

2. **Data Cleaning**
   - Remove duplicates
   - Strip whitespace from strings
   - Handle null values in critical fields

3. **Salary Parsing**
   - Extract salary_min and salary_max from ranges
   - Handle formats: "$80K - $120K", "80000-120000", "Competitive"
   - Convert all to annual amounts in USD

4. **Location Parsing**
   - Split into city, state, country
   - Standardize state abbreviations
   - Identify remote positions (is_remote flag)
   - Assign regions (Northeast, West Coast, etc.)

5. **Job Categorization**
   - Derive seniority_level from title keywords
   - Assign job_category (Data Analytics, Data Science, BI, etc.)

6. **Employment Type Normalization**
   - Standardize employment_type values
   - Identify work_arrangement (Remote, Hybrid, On-site)

7. **Skill Extraction**
   - Parse skills from job description or dedicated skills column
   - Create unique skill list
   - Categorize skills (Programming, BI Tools, Cloud, etc.)
   - Build posting-skill mappings

8. **Dimension Creation**
   - Deduplicate to create unique dimension records
   - Assign surrogate keys
   - Maintain referential integrity

**Outputs:** (to `data/interim/`)
- `job_postings_cleaned.csv` (fact table base)
- `dim_job.csv`
- `dim_company.csv`
- `dim_location.csv`
- `dim_employment_type.csv`
- `dim_skill.csv`
- `bridge_posting_skill.csv`

---

### Stage 3: Database Load

**Objective:** Load cleaned data into SQLite for SQL transformations

**Technology:** Python (sqlite3 or sqlalchemy)

**Input:** All CSV files from `data/interim/`

**Process:**
1. Create SQLite connection (`job_market.db`)
2. For each CSV file:
   - Read with pandas
   - Load into staging table using `to_sql()`
   - Use `if_exists='replace'` to allow re-runs
3. Display row counts for verification

**Output:** `job_market.db` with staging tables populated

**Naming Convention:**
- `stg_dim_job`
- `stg_dim_company`
- `stg_fact_posting`
- etc.

---

### Stage 4: Dimensional Model Creation

**Objective:** Define the star schema structure

**Technology:** SQL (SQLite)

**Input:** None (creates empty tables)

**Process:**
1. DROP existing dimensional tables (clean slate)
2. CREATE dimension tables with:
   - Primary keys (surrogate keys)
   - Data type definitions
   - NOT NULL constraints where appropriate
3. CREATE fact table with:
   - Primary key
   - Foreign key constraints to dimensions
   - Measure columns (salary_min, salary_max)
4. CREATE bridge table with composite primary key

**Output:** Empty dimensional model tables in `job_market.db`

**Script:** `sql/create_tables.sql`

---

### Stage 5: Data Transformation

**Objective:** Populate dimensional model from staging tables

**Technology:** SQL (SQLite)

**Input:** Staging tables from Stage 3

**Process:**
1. **Populate Dimensions**
   - INSERT INTO dim_* from stg_dim_*
   - May include deduplication if not done in Python

2. **Populate Fact Table**
   - INSERT INTO fact_posting from stg_fact_posting
   - JOIN to dimensions to get surrogate keys (if needed)
   - Apply business rules (e.g., salary_min <= salary_max)

3. **Populate Bridge Table**
   - INSERT INTO bridge_posting_skill from staging

4. **Data Quality Checks**
   - Check for orphaned records (FK integrity)
   - Validate null values in required fields
   - Check for salary outliers

5. **Summary Statistics**
   - Display row counts for all tables

**Output:** Fully populated dimensional model

**Script:** `sql/staging_transforms.sql`

---

### Stage 6: Analytical Views

**Objective:** Create pre-aggregated views for Power BI consumption

**Technology:** SQL (SQLite)

**Input:** Populated dimensional model

**Process:**
1. CREATE VIEW vw_job_posting_details
   - Denormalized view with all dimensions joined
   - Calculated column: salary_midpoint

2. CREATE VIEW vw_salary_by_title_and_location
   - Aggregated salary stats by job title and location
   - Metrics: avg, min, max salary

3. CREATE VIEW vw_skill_demand
   - Skills ranked by posting count
   - Join through bridge table

4. CREATE VIEW vw_remote_vs_onsite_trends
   - Work arrangement breakdown over time (if date available)
   - Percentage calculations

**Output:** Analytical views optimized for BI queries

**Script:** `sql/analytics_views.sql`

---

### Stage 7: Power Query Transformation

**Objective:** Load data into Power BI and apply final shaping

**Technology:** Power Query (M language)

**Input:** SQLite views OR processed CSV files

**Process:**

**Option A: SQLite Connection**
1. Connect to `job_market.db` using ODBC
2. Load analytical views
3. Apply transformations:
   - Set data types
   - Add derived columns (salary bands, date intelligence)
   - Filter for recent data (e.g., last 12 months)

**Option B: CSV Import**
1. Load fact and dimension CSVs from `data/processed/`
2. Promote headers and set data types
3. Create relationships in Power BI Model view
4. Add calculated columns

**Output:** Power Query tables in Power BI data model

**Reference:** `power_query/job_postings_power_query_m_code.txt`

---

### Stage 8: Visualization

**Objective:** Build interactive dashboard

**Technology:** Power BI Desktop

**Input:** Power Query tables

**Process:**
1. Import data from Power Query
2. Define DAX measures for KPIs
3. Create dashboard pages:
   - Overview (KPIs, trends)
   - Skills Deep Dive
   - Compensation Analysis
   - Geographic Insights
   - Work Arrangement Trends
4. Add slicers, filters, drill-through
5. Apply visual theme and branding

**Output:** `Job_Market_Analytics_Dashboard.pbix`

**Reference:** `bi/README_bi_layer.md`, `docs/dashboard_design.md`

---

## Execution Workflow

### Manual Execution (Current)

```bash
# Step 1: Add raw data
# Place job_postings_raw.csv in data/raw/

# Step 2: Run Python ETL scripts
python python/01_ingest_raw_files.py
python python/02_clean_and_normalize.py
python python/03_export_for_sql_load.py

# Step 3: Execute SQL scripts
# Option A: Use SQLite CLI
sqlite3 job_market.db < sql/create_tables.sql
sqlite3 job_market.db < sql/staging_transforms.sql
sqlite3 job_market.db < sql/analytics_views.sql

# Option B: Use DB Browser for SQLite (GUI)
# Open job_market.db and run scripts manually

# Step 4: Open Power BI and connect
# Use M code from power_query/ folder

# Step 5: Build dashboard
```

### Future: Automated Execution (Apache Airflow DAG)

```python
# Example Airflow DAG structure
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

dag = DAG('job_market_etl', schedule_interval='@weekly')

ingest = PythonOperator(
    task_id='ingest_raw_files',
    python_callable=run_ingestion,
    dag=dag
)

clean = PythonOperator(
    task_id='clean_and_normalize',
    python_callable=run_cleaning,
    dag=dag
)

load_db = PythonOperator(
    task_id='load_to_sqlite',
    python_callable=run_db_load,
    dag=dag
)

create_tables = BashOperator(
    task_id='create_tables',
    bash_command='sqlite3 job_market.db < sql/create_tables.sql',
    dag=dag
)

# Define task dependencies
ingest >> clean >> load_db >> create_tables
```

---

## Data Flow Summary

| Stage | Input | Output | Tech | Duration* |
|-------|-------|--------|------|-----------|
| 1. Ingestion | Raw CSV (Kaggle) | Combined raw CSV | Python | < 1 min |
| 2. Cleaning | Combined raw CSV | Dimensional CSVs | Python | 2-5 min |
| 3. DB Load | Dimensional CSVs | SQLite staging tables | Python | < 1 min |
| 4. Schema | None | Empty dimensional tables | SQL | < 1 sec |
| 5. Transform | Staging tables | Populated dimensions/fact | SQL | 1-2 min |
| 6. Views | Dimensional model | Analytical views | SQL | < 1 sec |
| 7. Power Query | SQLite/CSV | Power BI tables | M | < 1 min |
| 8. Visualization | Power BI tables | Dashboard | Power BI | 30-60 min |

*Duration estimates for ~50,000 job postings

---

## Error Handling Strategy

### Python Scripts
- **File Not Found:** Exit with clear error message and instructions
- **Data Quality Issues:** Log warnings but continue (e.g., unparseable salaries)
- **Schema Changes:** Gracefully handle missing columns (use defaults)

### SQL Scripts
- **Foreign Key Violations:** Prevented by data quality checks in staging
- **Duplicate Keys:** Handled by PRIMARY KEY constraints
- **Orphaned Records:** Identified in data quality checks, logged

### Power BI
- **Connection Failures:** Provide clear error messages about file paths
- **Data Type Mismatches:** Explicitly set types in Power Query

---

## Dependencies

### Software Requirements
- Python 3.8+
- SQLite (included with Python)
- Power BI Desktop (free)

### Python Libraries
- pandas >= 1.5.0
- sqlalchemy >= 1.4.0
- python-dotenv >= 0.19.0

### Optional Tools
- DB Browser for SQLite (GUI for database inspection)
- SQLite ODBC driver (for Power BI direct connection)
- Apache Airflow (for orchestration)

---

## Performance Considerations

### For Small Datasets (< 50K rows)
- Current design is sufficient
- Full refresh is fast (< 5 minutes end-to-end)

### For Large Datasets (> 500K rows)
- Consider chunking in pandas (`chunksize` parameter)
- Use indexes on frequently filtered columns
- Implement incremental loading (append only new records)
- Consider using PostgreSQL instead of SQLite

---

## Future Enhancements

1. **Incremental Loading**
   - Track last refresh date
   - Only process new/updated postings

2. **Data Validation Layer**
   - Add schema validation (e.g., using Pydantic)
   - Implement data quality rules engine

3. **Logging & Monitoring**
   - Replace print statements with proper logging
   - Track ETL run metadata (start time, end time, rows processed)

4. **Orchestration**
   - Implement Airflow DAG for scheduling
   - Add retry logic and alerting

5. **Testing**
   - Unit tests for Python functions
   - Integration tests for end-to-end pipeline
   - Data quality tests (Great Expectations)

6. **Documentation Auto-Generation**
   - Generate data dictionary from database schema
   - Create lineage diagrams automatically

---

**Last Updated:** 2024
**Author:** Analytics Portfolio Project
