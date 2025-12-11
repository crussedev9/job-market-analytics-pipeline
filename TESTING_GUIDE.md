# Testing Guide: Running the Pipeline with Glassdoor Dataset

This guide walks you through testing the Job Market Analytics Pipeline with real data from Kaggle.

## 📊 Dataset Information

**Dataset:** Data Science Job Postings on Glassdoor
**Source:** https://www.kaggle.com/datasets/andresionek/data-science-job-postings-on-glassdoor
**Size:** ~600-1000 job postings
**Fields:** Job titles, salaries, locations, company info, job descriptions

---

## 🚀 Quick Start (5 Steps)

### Step 1: Download the Dataset

#### Option A: Manual Download (Easiest)

1. Go to https://www.kaggle.com/datasets/andresionek/data-science-job-postings-on-glassdoor
2. Sign in to Kaggle (create free account if needed)
3. Click **Download** button (top right)
4. Extract the ZIP file
5. Find the CSV file (likely named `Uncleaned_DS_jobs.csv` or `DataScientist.csv`)
6. Copy it to: `data/raw/job_postings_raw.csv`

```bash
# Windows
copy "path\to\downloaded\file.csv" "data\raw\job_postings_raw.csv"
```

#### Option B: Kaggle API (Advanced)

```bash
# Install Kaggle package
pip install kaggle

# Set up API credentials
# 1. Go to https://www.kaggle.com/account
# 2. Click "Create New API Token"
# 3. Save kaggle.json to C:\Users\<username>\.kaggle\

# Run download script
python download_dataset.py
```

---

### Step 2: Set Up Python Environment

```bash
# Navigate to project directory
cd C:\Users\ckrus\job-market-analytics-pipeline

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3: Run the Python ETL Pipeline

```bash
# Step 3a: Ingest raw data
python python/01_ingest_raw_files.py

# Expected output:
# ✓ Found raw data file
# ✓ Successfully loaded X rows
# ✓ Saved combined raw data

# Step 3b: Clean and normalize (Glassdoor-specific version)
python python/02_clean_and_normalize_glassdoor.py

# Expected output:
# ✓ Parsed X salaries
# ✓ Parsed locations
# ✓ Extracted X unique skills
# ✓ Created dimension tables

# Step 3c: Load into SQLite
python python/03_export_for_sql_load.py

# Expected output:
# ✓ Loaded X rows into stg_dim_job
# ✓ Loaded X rows into stg_dim_company
# ✓ Database created: job_market.db
```

---

### Step 4: Run SQL Transformations

#### Option A: Using SQLite Command Line

```bash
# Navigate to project root
cd C:\Users\ckrus\job-market-analytics-pipeline

# Run SQL scripts in order
sqlite3 job_market.db < sql/create_tables.sql
sqlite3 job_market.db < sql/staging_transforms.sql
sqlite3 job_market.db < sql/analytics_views.sql

# Verify tables were created
sqlite3 job_market.db "SELECT name FROM sqlite_master WHERE type='table';"
```

#### Option B: Using DB Browser for SQLite (GUI)

1. **Download DB Browser:** https://sqlitebrowser.org/dl/
2. **Open database:** File → Open Database → `job_market.db`
3. **Execute scripts:**
   - File → Execute SQL
   - Load and run `sql/create_tables.sql`
   - Load and run `sql/staging_transforms.sql`
   - Load and run `sql/analytics_views.sql`
4. **Browse data:** Click "Browse Data" tab to see tables

---

### Step 5: Explore the Data

#### Quick Data Checks (SQL Queries)

Open SQLite CLI or DB Browser and run:

```sql
-- Check fact table row count
SELECT COUNT(*) AS total_postings FROM fact_posting;

-- Top 10 skills
SELECT
    s.skill_name,
    COUNT(*) AS posting_count
FROM dim_skill s
JOIN bridge_posting_skill b ON s.skill_id = b.skill_id
GROUP BY s.skill_name
ORDER BY posting_count DESC
LIMIT 10;

-- Average salary by job category
SELECT
    j.job_category,
    COUNT(*) AS postings,
    ROUND(AVG((f.salary_min + f.salary_max) / 2.0), 0) AS avg_salary
FROM fact_posting f
JOIN dim_job j ON f.job_id = j.job_id
WHERE f.salary_min IS NOT NULL
GROUP BY j.job_category
ORDER BY avg_salary DESC;

-- Top locations
SELECT
    l.city,
    l.state,
    COUNT(*) AS posting_count
FROM fact_posting f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY l.city, l.state
ORDER BY posting_count DESC
LIMIT 10;

-- Remote vs on-site
SELECT
    CASE WHEN l.is_remote = 1 THEN 'Remote' ELSE 'On-site' END AS work_type,
    COUNT(*) AS postings,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_posting), 1) AS percentage
FROM fact_posting f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY l.is_remote;
```

---

## 📊 Expected Results

After running the pipeline, you should have:

### Dimensional Model Tables

| Table | Expected Rows | Description |
|-------|--------------|-------------|
| `fact_posting` | 600-1000 | One row per job posting |
| `dim_job` | 200-400 | Unique job titles |
| `dim_company` | 300-600 | Unique companies |
| `dim_location` | 100-200 | Unique locations |
| `dim_employment_type` | 3-5 | Employment types |
| `dim_skill` | 40-80 | Skills extracted from descriptions |
| `bridge_posting_skill` | 3000-8000 | Posting-skill mappings |

### Analytical Views

| View | Description |
|------|-------------|
| `vw_job_posting_details` | Denormalized posting details |
| `vw_salary_by_title_and_location` | Salary aggregations |
| `vw_skill_demand` | Skills ranked by demand |
| `vw_remote_vs_onsite_trends` | Work arrangement breakdown |

---

## 🔍 Troubleshooting

### Issue: "File not found: job_postings_raw.csv"

**Solution:**
- Ensure you downloaded the Kaggle dataset
- Check the file is in `data/raw/` folder
- Verify it's named exactly `job_postings_raw.csv`

### Issue: "ModuleNotFoundError: No module named 'config_glassdoor_dataset'"

**Solution:**
```bash
# Make sure you're in the project root
cd C:\Users\ckrus\job-market-analytics-pipeline

# Run from project root
python python/02_clean_and_normalize_glassdoor.py
```

### Issue: "Column not found" errors

**Solution:**
- The Glassdoor dataset may have different column names
- Open `data/raw/job_postings_raw.csv` in Excel
- Compare columns to `config_glassdoor_dataset.py` → `COLUMN_MAPPING`
- Update the mapping if needed

### Issue: SQL foreign key violations

**Solution:**
```sql
-- Check for orphaned records
SELECT COUNT(*)
FROM fact_posting f
LEFT JOIN dim_job j ON f.job_id = j.job_id
WHERE j.job_id IS NULL;

-- If found, re-run the cleaning script
```

### Issue: No skills extracted

**Solution:**
- This is normal if job descriptions are very short
- Check `dim_skill` table - should have 40-80 skills
- If 0 skills, check that `job_description` column exists

---

## 📈 Next Steps: Power BI Dashboard

Once the pipeline runs successfully:

### 1. Open Power BI Desktop

Download from: https://powerbi.microsoft.com/desktop/

### 2. Connect to Data

**Option A: Connect to SQLite (Recommended)**

1. Get Data → More → ODBC
2. Install SQLite ODBC driver if needed
3. Connection string: `Driver={SQLite3 ODBC Driver};Database=C:\Users\ckrus\job-market-analytics-pipeline\job_market.db`
4. Select analytical views to import

**Option B: Import CSV Files**

1. Get Data → Text/CSV
2. Load tables from `data/processed/` (if you export them)
3. Create relationships in Model view

### 3. Use Power Query Template

1. In Power BI: Transform Data → Advanced Editor
2. Open `power_query/job_postings_power_query_m_code.txt`
3. Copy the appropriate code block
4. Paste into Advanced Editor
5. Update file paths

### 4. Build Dashboard

Follow specifications in:
- `bi/README_bi_layer.md` - Dashboard overview
- `docs/dashboard_design.md` - Detailed page layouts

---

## 🧪 Data Quality Checks

Run these to validate your data:

```sql
-- 1. Check for nulls in critical fields
SELECT
    SUM(CASE WHEN job_id IS NULL THEN 1 ELSE 0 END) AS null_job_ids,
    SUM(CASE WHEN company_id IS NULL THEN 1 ELSE 0 END) AS null_company_ids,
    SUM(CASE WHEN location_id IS NULL THEN 1 ELSE 0 END) AS null_location_ids
FROM fact_posting;

-- 2. Salary data completeness
SELECT
    COUNT(*) AS total_postings,
    SUM(CASE WHEN salary_min IS NOT NULL THEN 1 ELSE 0 END) AS with_salary,
    ROUND(SUM(CASE WHEN salary_min IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_with_salary
FROM fact_posting;

-- 3. Skill extraction success rate
SELECT
    COUNT(DISTINCT posting_id) AS postings_with_skills,
    (SELECT COUNT(*) FROM fact_posting) AS total_postings,
    ROUND(COUNT(DISTINCT posting_id) * 100.0 / (SELECT COUNT(*) FROM fact_posting), 1) AS pct_with_skills
FROM bridge_posting_skill;

-- 4. Validate dimension integrity
-- All job_ids in fact table should exist in dim_job
SELECT COUNT(*) AS orphaned_jobs
FROM fact_posting f
LEFT JOIN dim_job j ON f.job_id = j.job_id
WHERE j.job_id IS NULL;
-- Result should be 0
```

---

## 📝 Sample Insights You Can Get

Once the pipeline is complete, you can answer:

- **"What are the top 10 most in-demand skills?"** → Query `vw_skill_demand`
- **"What's the average salary for Senior Data Scientists in California?"** → Query with filters
- **"Which companies are hiring the most?"** → Group by company
- **"What % of jobs are remote?"** → Aggregate `is_remote` flag
- **"Which skills correlate with higher salaries?"** → Join skills with salary data

---

## 🎯 Success Criteria

Your pipeline is working correctly if:

- ✅ All Python scripts run without errors
- ✅ `job_market.db` file is created (should be 1-5 MB)
- ✅ All 7 tables exist and have data
- ✅ All 4 analytical views exist
- ✅ Sample SQL queries return sensible results
- ✅ No foreign key orphans (all FKs match dimension keys)

---

## 📚 Additional Resources

- **Glassdoor Dataset Discussion:** https://www.kaggle.com/datasets/andresionek/data-science-job-postings-on-glassdoor/discussion
- **SQLite Documentation:** https://www.sqlite.org/docs.html
- **Power BI Learning:** https://learn.microsoft.com/en-us/power-bi/
- **Star Schema Design:** Kimball's "Data Warehouse Toolkit"

---

## 💡 Pro Tips

1. **Save your SQL queries** - Create a `queries/` folder for common queries
2. **Document anomalies** - Note any weird data patterns you find
3. **Export samples** - Save sample outputs as CSVs for your portfolio
4. **Take screenshots** - Capture query results for your resume/LinkedIn
5. **Time yourself** - Track how long the full pipeline takes (good metric to share)

---

**Questions or Issues?**

- Check `README.md` for project overview
- Review `docs/pipeline_design.md` for architecture
- See `docs/data_model.md` for schema details

Good luck! 🚀
