# Quick Start Guide - Glassdoor Dataset

You've downloaded the comprehensive Glassdoor dataset (**165,290 job postings**). This is a large dataset, so here are two options:

---

## Option 1: Full Dataset (Recommended for Final Results)

Process all 165K+ records - gives you the most comprehensive insights.

**Runtime:** ~5-15 minutes total

```bash
# Activate virtual environment
cd C:\Users\ckrus\job-market-analytics-pipeline
venv\Scripts\activate

# Run pipeline
python python/01_ingest_raw_files.py
python python/02_clean_and_normalize_glassdoor.py
python python/03_export_for_sql_load.py
```

---

## Option 2: Sample Dataset (For Quick Testing)

Process a 10% sample (~16,500 records) for faster testing.

**Runtime:** ~1-3 minutes total

### Create Sample

```python
# Run this Python code to create a sample
import pandas as pd

# Load full dataset
df = pd.read_csv('data/raw/job_postings_raw.csv')

# Take 10% sample
sample_df = df.sample(frac=0.10, random_state=42)

# Save sample
sample_df.to_csv('data/raw/job_postings_raw_BACKUP.csv', index=False)  # Backup full
sample_df.to_csv('data/raw/job_postings_raw.csv', index=False)  # Replace with sample

print(f"Sample created: {len(sample_df):,} rows")
```

Then run the pipeline normally.

---

## What to Expect

### Dataset Columns

This Glassdoor export has nested column names:
- `gaTrackerData.jobTitle` - Job titles
- `gaTrackerData.location` - Location
- `gaTrackerData.empName` - Company names
- `job.description` - Full job descriptions
- `header.payHigh` / `header.payLow` - Salary ranges
- `overview.size` - Company size
- `overview.industry` - Industry
- And many more...

### After Processing

You'll have:
- **~165K job postings** in fact table
- **~60-100 unique skills** extracted
- **~50K+ companies** (many companies post multiple jobs)
- **~5K+ unique locations**
- **~3-5M posting-skill mappings** in bridge table

---

## Step-by-Step Execution

### Step 1: Install Dependencies

```bash
cd C:\Users\ckrus\job-market-analytics-pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Verify Data File

```bash
# Check file exists
dir data\raw\job_postings_raw.csv

# Should show ~8MB file
```

### Step 3: Run Python Scripts

```bash
# Ingest (30 seconds)
python python/01_ingest_raw_files.py

# Clean (5-10 minutes for full dataset)
python python/02_clean_and_normalize_glassdoor.py

# Load to SQLite (1-2 minutes)
python python/03_export_for_sql_load.py
```

### Step 4: Run SQL Scripts

```bash
# Create tables
sqlite3 job_market.db < sql/create_tables.sql

# Transform data (may take a few minutes)
sqlite3 job_market.db < sql/staging_transforms.sql

# Create views
sqlite3 job_market.db < sql/analytics_views.sql
```

### Step 5: Verify Success

```bash
sqlite3 job_market.db

# Run test query
SELECT COUNT(*) FROM fact_posting;
# Should return ~165,290 (or ~16,500 if you used sample)

# Top skills
SELECT s.skill_name, COUNT(*) as count
FROM dim_skill s
JOIN bridge_posting_skill b ON s.skill_id = b.skill_id
GROUP BY s.skill_name
ORDER BY count DESC
LIMIT 10;
```

---

## Expected Insights

With this large dataset, you can find:

- **Most in-demand skills:** SQL, Python, Excel typically top the list
- **Salary ranges by role:** Data Scientists avg $110-130K, Analysts $70-90K
- **Remote work trends:** Likely 30-40% of analytics roles are remote
- **Geographic concentration:** California, New York, Texas dominate
- **Company insights:** Tech companies vs Finance vs Retail salary differences

---

## Troubleshooting

### "Takes too long to run"
- Use Option 2 (sample dataset) for testing
- Or run overnight for full results

### "Out of memory" error
- Close other applications
- Use sample dataset
- Or increase Python memory limit

### "Columns not found"
- The dataset might have slightly different columns
- Check `config_glassdoor_dataset.py` and update `COLUMN_MAPPING` if needed

### SQL script errors
- Make sure Python scripts completed successfully first
- Check `job_market.db` file was created
- Try running SQL in DB Browser (GUI) to see specific errors

---

## Performance Tips

**For 165K records:**
- Script 01 (Ingest): ~30 seconds
- Script 02 (Clean): ~8-12 minutes (skill extraction is slow)
- Script 03 (Load): ~1-2 minutes
- SQL transforms: ~3-5 minutes
- **Total: ~15-20 minutes**

**To speed up:**
1. Use sample dataset for initial testing
2. Comment out skill extraction temporarily (fastest bottleneck)
3. Run on SSD drive if possible
4. Close other applications

---

## Next Steps After Success

1. **Explore the data:**
   ```sql
   -- Average salary by job category
   SELECT j.job_category, ROUND(AVG((f.salary_min + f.salary_max)/2), 0) as avg_sal
   FROM fact_posting f
   JOIN dim_job j ON f.job_id = j.job_id
   WHERE f.salary_min IS NOT NULL
   GROUP BY j.job_category
   ORDER BY avg_sal DESC;
   ```

2. **Export insights to Excel:**
   ```bash
   sqlite3 -header -csv job_market.db "SELECT * FROM vw_skill_demand LIMIT 50;" > top_skills.csv
   ```

3. **Build Power BI dashboard:**
   - Open Power BI Desktop
   - Get Data → SQLite
   - Connect to `job_market.db`
   - Import analytical views
   - Follow `docs/dashboard_design.md` for layout

4. **Add to your portfolio:**
   - Take screenshots of top insights
   - Document key findings in README
   - Add to LinkedIn/resume

---

**Ready? Start with Step 1!** 🚀

If you encounter any issues, check [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed troubleshooting.
