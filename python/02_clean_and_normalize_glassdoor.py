"""
Job Market Analytics Pipeline - Step 2: Clean and Normalize (Glassdoor Dataset)

This is an enhanced version specifically for the Glassdoor Data Science Jobs dataset.
It implements actual parsing logic for salary, location, skills, etc.

Author: Analytics Portfolio Project
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import re

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
from config_glassdoor_dataset import (
    COLUMN_MAPPING, SKILLS_DICT, JOB_TITLE_GROUPS,
    SENIORITY_KEYWORDS, REMOTE_KEYWORDS, EMPLOYMENT_KEYWORDS,
    COMPANY_SIZE_MAPPING
)


def setup_paths() -> dict:
    """Set up project paths."""
    project_root = Path(__file__).parent.parent
    paths = {
        'input_csv': project_root / 'data' / 'interim' / 'job_postings_raw_combined.csv',
        'output_dir': project_root / 'data' / 'interim',
    }
    return paths


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Map Glassdoor column names to our schema."""
    print("Normalizing column names...")

    # Try to rename using mapping
    df = df.rename(columns=COLUMN_MAPPING)

    # Also normalize any remaining columns
    df.columns = (df.columns
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace('-', '_')
                  .str.replace(r'[^a-z0-9_]', '', regex=True))

    print(f"✓ Columns after normalization: {list(df.columns)}")
    return df


def parse_salary_from_fields(row):
    """
    Parse salary from the nested Glassdoor fields.

    Priority:
    1. Use salary_high/salary_low if available (annual)
    2. Fall back to pay_high/pay_low if payPeriod is yearly
    3. Convert hourly to annual if needed
    """
    salary_low = row.get('salary_low')
    salary_high = row.get('salary_high')
    pay_low = row.get('pay_low')
    pay_high = row.get('pay_high')
    pay_period = str(row.get('pay_period', '')).lower()

    # Try salary fields first (these are annual)
    if pd.notna(salary_low) and pd.notna(salary_high):
        try:
            return float(salary_low), float(salary_high), 'USD'
        except:
            pass

    # Try pay fields
    if pd.notna(pay_low) and pd.notna(pay_high):
        try:
            low = float(pay_low)
            high = float(pay_high)

            # Convert based on period
            if 'hour' in pay_period:
                # Assume 40 hours/week, 52 weeks/year
                low = low * 40 * 52
                high = high * 40 * 52
            elif 'month' in pay_period:
                low = low * 12
                high = high * 12
            # If yearly or empty, use as-is

            return low, high, 'USD'
        except:
            pass

    return None, None, 'USD'


def parse_location(location_str):
    """
    Parse location string.

    Examples:
    - "San Francisco, CA" → city="San Francisco", state="CA"
    - "New York, NY" → city="New York", state="NY"
    - "Remote" → city="Remote", state=None
    """
    if pd.isna(location_str):
        return None, None, 'USA', False

    location_str = str(location_str).strip()

    # Check for remote
    is_remote = any(keyword in location_str.lower() for keyword in REMOTE_KEYWORDS)

    if is_remote:
        return 'Remote', None, 'USA', True

    # Parse "City, ST" format
    parts = location_str.split(',')
    if len(parts) >= 2:
        city = parts[0].strip()
        state = parts[1].strip()
        return city, state, 'USA', False

    # Single value (assume it's city)
    return location_str, None, 'USA', False


def derive_seniority(job_title):
    """Derive seniority level from job title."""
    if pd.isna(job_title):
        return 'Mid-level'

    title_lower = str(job_title).lower()

    for level, keywords in SENIORITY_KEYWORDS.items():
        if any(keyword in title_lower for keyword in keywords):
            return level

    return 'Mid-level'  # Default


def categorize_job_title(job_title):
    """Categorize job title into broad groups."""
    if pd.isna(job_title):
        return 'Other'

    title_lower = str(job_title).lower()

    for category, keywords in JOB_TITLE_GROUPS.items():
        if any(keyword in title_lower for keyword in keywords):
            return category

    return 'Other'


def extract_skills_from_description(description):
    """Extract skills from job description text."""
    if pd.isna(description):
        return []

    description_lower = str(description).lower()
    found_skills = []

    # Search for all skills
    for category, skills in SKILLS_DICT.items():
        for skill in skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, description_lower):
                found_skills.append(skill)

    return list(set(found_skills))  # Remove duplicates


def clean_company_size(size_str):
    """Standardize company size."""
    if pd.isna(size_str) or size_str == '-1' or size_str == 'Unknown':
        return 'Unknown'

    size_str = str(size_str).strip()

    # Check mapping
    if size_str in COMPANY_SIZE_MAPPING:
        return COMPANY_SIZE_MAPPING[size_str]

    return size_str


def main():
    """Main execution flow."""
    print("="*70)
    print("JOB MARKET ANALYTICS - STEP 2: CLEAN & NORMALIZE (GLASSDOOR)")
    print("="*70)

    paths = setup_paths()

    # Load data
    print(f"\nLoading data from: {paths['input_csv']}")
    try:
        df = pd.read_csv(paths['input_csv'])
        print(f"✓ Loaded {len(df):,} rows")
    except FileNotFoundError:
        print(f"ERROR: Input file not found. Please run 01_ingest_raw_files.py first.")
        sys.exit(1)

    # Normalize columns
    df = normalize_column_names(df)

    # Parse salary from nested fields
    print("\nParsing salaries...")
    df[['salary_min', 'salary_max', 'salary_currency']] = df.apply(
        lambda row: pd.Series(parse_salary_from_fields(row)),
        axis=1
    )
    salary_parsed = df['salary_min'].notna().sum()
    print(f"  ✓ Parsed {salary_parsed:,} / {len(df):,} salaries ({salary_parsed/len(df)*100:.1f}%)")

    # Parse location
    print("\nParsing locations...")
    df[['city', 'state', 'country', 'is_remote']] = df.apply(
        lambda row: pd.Series(parse_location(row.get('location'))),
        axis=1
    )
    print(f"  ✓ Parsed locations")
    print(f"  Remote jobs: {df['is_remote'].sum():,}")

    # Derive job attributes
    print("\nDeriving job attributes...")
    df['seniority_level'] = df['job_title'].apply(derive_seniority)
    df['job_category'] = df['job_title'].apply(categorize_job_title)

    print(f"  Job categories:")
    for cat, count in df['job_category'].value_counts().head(5).items():
        print(f"    - {cat}: {count:,}")

    # Extract skills
    print("\nExtracting skills from job descriptions...")
    df['skills_list'] = df.get('job_description', pd.Series()).apply(extract_skills_from_description)
    df['skill_count'] = df['skills_list'].apply(len)
    print(f"  ✓ Avg skills per posting: {df['skill_count'].mean():.1f}")

    # Clean company data
    print("\nCleaning company data...")
    df['company_size_clean'] = df.get('company_size', pd.Series()).apply(clean_company_size)

    # Create unique ID
    df['posting_id'] = range(1, len(df) + 1)

    # Create dimension tables
    print("\nCreating dimension tables...")

    # dim_job
    dim_job = df[['job_title', 'job_category', 'seniority_level']].drop_duplicates().reset_index(drop=True)
    dim_job.insert(0, 'job_id', range(1, len(dim_job) + 1))
    print(f"  ✓ dim_job: {len(dim_job):,} unique jobs")

    # dim_company
    company_cols = ['company_name', 'company_rating', 'company_size_clean', 'ownership_type', 'industry', 'sector', 'revenue']
    available_company_cols = [col for col in company_cols if col in df.columns]
    dim_company = df[available_company_cols].drop_duplicates(subset=['company_name']).reset_index(drop=True)
    dim_company.insert(0, 'company_id', range(1, len(dim_company) + 1))
    print(f"  ✓ dim_company: {len(dim_company):,} unique companies")

    # dim_location
    dim_location = df[['city', 'state', 'country', 'is_remote']].drop_duplicates().reset_index(drop=True)
    dim_location.insert(0, 'location_id', range(1, len(dim_location) + 1))
    # Add region (simplified)
    dim_location['region'] = dim_location['state'].apply(lambda x: 'Northeast' if x in ['NY', 'MA', 'PA', 'NJ'] else 'Other')
    print(f"  ✓ dim_location: {len(dim_location):,} unique locations")

    # dim_employment_type (simplified - all full-time for this dataset)
    dim_employment_type = pd.DataFrame({
        'employment_type_id': [1, 2, 3],
        'employment_type': ['Full-time', 'Contract', 'Internship'],
        'work_arrangement': ['On-site', 'Remote', 'Hybrid']
    })
    print(f"  ✓ dim_employment_type: {len(dim_employment_type):,} types")

    # dim_skill
    all_skills = []
    for skills in df['skills_list']:
        all_skills.extend(skills)
    unique_skills = sorted(set(all_skills))

    dim_skill = pd.DataFrame({'skill_name': unique_skills})
    dim_skill.insert(0, 'skill_id', range(1, len(dim_skill) + 1))

    # Add skill category
    def get_skill_category(skill):
        for category, skills in SKILLS_DICT.items():
            if skill in skills:
                return category
        return 'Other'

    dim_skill['skill_category'] = dim_skill['skill_name'].apply(get_skill_category)
    print(f"  ✓ dim_skill: {len(dim_skill):,} unique skills")

    # bridge_posting_skill
    bridge_rows = []
    for idx, row in df.iterrows():
        posting_id = row['posting_id']
        for skill in row['skills_list']:
            skill_id = dim_skill[dim_skill['skill_name'] == skill]['skill_id'].values[0]
            bridge_rows.append({'posting_id': posting_id, 'skill_id': skill_id})

    bridge_posting_skill = pd.DataFrame(bridge_rows)
    print(f"  ✓ bridge_posting_skill: {len(bridge_posting_skill):,} mappings")

    # Create fact table with foreign keys
    print("\nCreating fact table with foreign keys...")

    # Merge to get foreign keys
    fact_posting = df.copy()

    # Get job_id
    fact_posting = fact_posting.merge(
        dim_job[['job_id', 'job_title', 'job_category', 'seniority_level']],
        on=['job_title', 'job_category', 'seniority_level'],
        how='left'
    )

    # Get company_id
    fact_posting = fact_posting.merge(
        dim_company[['company_id', 'company_name']],
        on='company_name',
        how='left'
    )

    # Get location_id
    fact_posting = fact_posting.merge(
        dim_location[['location_id', 'city', 'state', 'country', 'is_remote']],
        on=['city', 'state', 'country', 'is_remote'],
        how='left'
    )

    # Select fact table columns
    fact_cols = [
        'posting_id', 'job_id', 'company_id', 'location_id',
        'salary_min', 'salary_max', 'salary_currency'
    ]

    # Add employment_type_id (default to 1 for full-time)
    fact_posting['employment_type_id'] = 1  # Default: Full-time, On-site
    fact_cols.append('employment_type_id')

    # Add optional columns if they exist
    if 'easy_apply' in fact_posting.columns:
        fact_cols.append('easy_apply')

    fact_posting_clean = fact_posting[fact_cols]
    print(f"  ✓ fact_posting: {len(fact_posting_clean):,} records")

    # Save outputs
    print("\nSaving dimension tables and fact table...")
    paths['output_dir'].mkdir(parents=True, exist_ok=True)

    outputs = {
        'dim_job.csv': dim_job,
        'dim_company.csv': dim_company,
        'dim_location.csv': dim_location,
        'dim_employment_type.csv': dim_employment_type,
        'dim_skill.csv': dim_skill,
        'bridge_posting_skill.csv': bridge_posting_skill,
        'job_postings_cleaned.csv': fact_posting_clean,
    }

    for filename, df_out in outputs.items():
        filepath = paths['output_dir'] / filename
        df_out.to_csv(filepath, index=False)
        print(f"  ✓ Saved {filename} ({len(df_out):,} rows)")

    # Summary statistics
    print("\n" + "="*70)
    print("CLEANING SUMMARY")
    print("="*70)
    print(f"Total job postings: {len(df):,}")
    print(f"Jobs with salary data: {salary_parsed:,} ({salary_parsed/len(df)*100:.1f}%)")
    print(f"Remote positions: {df['is_remote'].sum():,} ({df['is_remote'].sum()/len(df)*100:.1f}%)")
    print(f"Unique companies: {len(dim_company):,}")
    print(f"Unique skills extracted: {len(dim_skill):,}")
    print(f"Average skills per job: {df['skill_count'].mean():.1f}")
    print(f"\nTop 5 skills:")
    skill_counts = bridge_posting_skill['skill_id'].value_counts().head(5)
    for skill_id, count in skill_counts.items():
        skill_name = dim_skill[dim_skill['skill_id'] == skill_id]['skill_name'].values[0]
        print(f"  {skill_name}: {count:,} postings")

    print("\n" + "="*70)
    print("STEP 2 COMPLETE: Data cleaned and dimensional tables created")
    print(f"Next step: Run python/03_export_for_sql_load.py")
    print("="*70)


if __name__ == "__main__":
    main()
