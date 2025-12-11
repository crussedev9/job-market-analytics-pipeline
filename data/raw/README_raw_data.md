# Raw Data Folder

This folder contains the original, unmodified job postings dataset from Kaggle.

## Expected File

**Filename:** `job_postings_raw.csv`

**Source:** Kaggle job postings dataset (user-supplied)

## Important Notes

- This file should be added manually before running the ETL pipeline
- The raw CSV file is **not included** in version control (see `.gitignore`)
- Do not modify files in this folder - they represent the source of truth

## Expected Schema

The raw CSV should contain the following columns (column names may vary):

- `job_id` or `id` - Unique identifier for the job posting
- `title` or `job_title` - Job title (e.g., "Senior Data Analyst")
- `company` or `company_name` - Company name
- `location` - Location string (e.g., "San Francisco, CA" or "Remote")
- `salary` or `salary_range` - Salary information (may need parsing)
- `employment_type` - Full-time, Contract, Part-time, etc.
- `remote_allowed` or `work_arrangement` - Remote, Hybrid, On-site
- `description` or `job_description` - Full job description text
- `skills` or `requirements` - Skills/requirements (may be embedded in description)
- `posted_date` or `date_posted` - When the job was posted
- `application_url` or `url` - Link to apply

## Data Source Recommendations

Suggested Kaggle datasets (search for):
- "Data Science Job Postings"
- "Job Postings from LinkedIn/Indeed/Glassdoor"
- "Tech Jobs Dataset"

## Usage

The Python script `python/01_ingest_raw_files.py` will read this CSV file as the first step in the ETL pipeline.
