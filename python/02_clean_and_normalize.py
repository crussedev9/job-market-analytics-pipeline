"""
Job Market Analytics Pipeline - Step 2: Clean and Normalize

This script reads the raw combined CSV, performs data cleaning and normalization,
and creates dimension tables and a fact table base for the star schema.

Outputs:
- job_postings_cleaned.csv (fact table base)
- dim_job.csv
- dim_company.csv
- dim_location.csv
- dim_employment_type.csv
- dim_skill.csv
- bridge_posting_skill.csv

Author: Analytics Portfolio Project
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import re


def setup_paths() -> dict:
    """Set up project paths."""
    project_root = Path(__file__).parent.parent

    paths = {
        'input_csv': project_root / 'data' / 'interim' / 'job_postings_raw_combined.csv',
        'output_dir': project_root / 'data' / 'interim',
    }

    return paths


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to lowercase snake_case.

    Args:
        df: DataFrame with original column names

    Returns:
        pd.DataFrame: DataFrame with normalized column names
    """
    print("Normalizing column names to lowercase snake_case...")

    df.columns = (df.columns
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace('-', '_')
                  .str.replace(r'[^a-z0-9_]', '', regex=True))

    print(f"✓ Normalized {len(df.columns)} column names")
    return df


def clean_job_postings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform general data cleaning on the job postings dataset.

    Args:
        df: Raw job postings DataFrame

    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    print("\nCleaning job postings data...")

    # TODO: Remove duplicate postings based on job_id or (title, company, location)
    initial_rows = len(df)
    # df = df.drop_duplicates(subset=['job_id'], keep='first')
    print(f"  TODO: Implement duplicate removal (currently {initial_rows:,} rows)")

    # TODO: Remove rows with critical null values
    # critical_columns = ['title', 'company']
    # df = df.dropna(subset=critical_columns)
    print(f"  TODO: Implement null value handling for critical columns")

    # TODO: Strip whitespace from string columns
    # string_cols = df.select_dtypes(include=['object']).columns
    # df[string_cols] = df[string_cols].apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
    print(f"  TODO: Implement whitespace stripping")

    return df


def parse_salary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse salary information into min, max, and currency fields.

    Args:
        df: DataFrame with salary column

    Returns:
        pd.DataFrame: DataFrame with parsed salary fields
    """
    print("\nParsing salary information...")

    # TODO: Implement salary parsing logic
    # Expected formats:
    # - "$80,000 - $120,000"
    # - "$100K - $150K"
    # - "80000-120000 USD"
    # - "Competitive"

    df['salary_min'] = np.nan
    df['salary_max'] = np.nan
    df['salary_currency'] = 'USD'

    print("  TODO: Implement salary range parsing from salary column")
    print("  TODO: Handle different formats (K notation, ranges, currencies)")
    print("  TODO: Convert all salaries to annual amounts")

    return df


def standardize_locations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse and standardize location information.

    Args:
        df: DataFrame with location column

    Returns:
        pd.DataFrame: DataFrame with parsed location fields
    """
    print("\nStandardizing location information...")

    # TODO: Parse location string into components
    # Examples:
    # - "San Francisco, CA" → city: San Francisco, state: CA, country: USA
    # - "Remote" → city: NULL, state: NULL, is_remote: True
    # - "New York, NY, USA" → city: New York, state: NY, country: USA

    df['city'] = None
    df['state'] = None
    df['country'] = 'USA'  # Default assumption
    df['is_remote'] = False

    print("  TODO: Implement location parsing logic")
    print("  TODO: Handle 'Remote' locations")
    print("  TODO: Standardize state abbreviations")
    print("  TODO: Infer country from location string")

    return df


def normalize_employment_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize employment type and work arrangement fields.

    Args:
        df: DataFrame with employment type information

    Returns:
        pd.DataFrame: DataFrame with normalized employment fields
    """
    print("\nNormalizing employment type...")

    # TODO: Standardize employment type values
    # Map variations to standard values:
    # - "Full-time", "Full Time", "FT" → "Full-time"
    # - "Contract", "Contractor", "Temporary" → "Contract"
    # - "Part-time", "Part Time", "PT" → "Part-time"

    df['employment_type'] = None  # Placeholder
    df['work_arrangement'] = None  # Remote, Hybrid, On-site

    print("  TODO: Implement employment type standardization")
    print("  TODO: Extract work arrangement (Remote/Hybrid/On-site)")
    print("  TODO: Handle cases where employment type is embedded in title")

    return df


def derive_seniority_level(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive seniority level from job title.

    Args:
        df: DataFrame with job title column

    Returns:
        pd.DataFrame: DataFrame with seniority_level field
    """
    print("\nDeriving seniority level from job titles...")

    # TODO: Implement seniority detection logic
    # Look for keywords in title:
    # - "Senior", "Sr.", "Sr" → Senior
    # - "Lead", "Principal", "Staff" → Lead
    # - "Junior", "Jr.", "Jr", "Associate" → Junior
    # - "Manager", "Director", "VP", "Chief" → Management
    # - Default → Mid-level

    df['seniority_level'] = 'Mid-level'  # Placeholder

    print("  TODO: Implement keyword-based seniority detection")
    print("  TODO: Handle edge cases (e.g., 'Senior Manager' vs 'Senior Analyst')")

    return df


def categorize_job_title(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize job titles into broad categories.

    Args:
        df: DataFrame with job title column

    Returns:
        pd.DataFrame: DataFrame with job_category field
    """
    print("\nCategorizing job titles...")

    # TODO: Implement job categorization
    # Categories:
    # - "Data Analytics" (Analyst, Business Intelligence, Analytics Engineer)
    # - "Data Science" (Data Scientist, ML Engineer)
    # - "Data Engineering" (Data Engineer, ETL Developer)
    # - "Business Intelligence" (BI Developer, BI Analyst)
    # - "Other"

    df['job_category'] = 'Data Analytics'  # Placeholder

    print("  TODO: Implement keyword-based job categorization")

    return df


def extract_skills(df: pd.DataFrame) -> tuple:
    """
    Extract skills from job descriptions or skills columns.

    Args:
        df: DataFrame with job description or skills column

    Returns:
        tuple: (DataFrame with posting_skill mappings, DataFrame with unique skills)
    """
    print("\nExtracting skills from job postings...")

    # TODO: Implement skill extraction
    # Approach 1: Split pre-existing skills column
    # Approach 2: Use keyword matching on job description
    # Common skills: Python, SQL, Power BI, Tableau, Excel, R, etc.

    # Placeholder: Create empty dataframes
    bridge_posting_skill = pd.DataFrame(columns=['posting_id', 'skill_id'])
    dim_skill = pd.DataFrame(columns=['skill_id', 'skill_name', 'skill_category'])

    print("  TODO: Implement skill extraction from description or skills column")
    print("  TODO: Create skill taxonomy (Programming, BI Tools, Cloud, etc.)")
    print("  TODO: Handle skill variations (e.g., 'PowerBI' vs 'Power BI')")

    return bridge_posting_skill, dim_skill


def create_dim_job(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the job dimension table.

    Args:
        df: Cleaned job postings DataFrame

    Returns:
        pd.DataFrame: Job dimension table
    """
    print("\nCreating dim_job...")

    # TODO: Adjust column names based on actual data
    dim_job = df[['job_category', 'seniority_level']].copy()

    # For demo purposes, create a simple dimension
    # In reality, you'd deduplicate and assign surrogate keys
    dim_job = dim_job.drop_duplicates().reset_index(drop=True)
    dim_job.insert(0, 'job_id', range(1, len(dim_job) + 1))

    print(f"  Created {len(dim_job):,} unique job records")
    print("  TODO: Add actual job_title column from source data")
    print("  TODO: Implement proper surrogate key assignment")

    return dim_job


def create_dim_company(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the company dimension table.

    Args:
        df: Cleaned job postings DataFrame

    Returns:
        pd.DataFrame: Company dimension table
    """
    print("\nCreating dim_company...")

    # TODO: Adjust based on actual column names in your dataset
    # Expected columns: company_name, industry, company_size

    dim_company = pd.DataFrame({
        'company_id': [1],
        'company_name': ['Placeholder Company'],
        'industry': ['Technology'],
        'company_size': ['Unknown']
    })

    print(f"  Created {len(dim_company):,} unique company records")
    print("  TODO: Extract unique companies from source data")
    print("  TODO: Add industry classification logic")
    print("  TODO: Add company size information if available")

    return dim_company


def create_dim_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the location dimension table.

    Args:
        df: Cleaned job postings DataFrame with parsed location fields

    Returns:
        pd.DataFrame: Location dimension table
    """
    print("\nCreating dim_location...")

    # TODO: Deduplicate locations and assign surrogate keys
    dim_location = pd.DataFrame({
        'location_id': [1, 2],
        'city': ['Remote', 'New York'],
        'state': [None, 'NY'],
        'country': ['USA', 'USA'],
        'region': ['N/A', 'Northeast'],
        'is_remote': [True, False]
    })

    print(f"  Created {len(dim_location):,} unique location records")
    print("  TODO: Extract unique locations from parsed location fields")
    print("  TODO: Add region classification (e.g., Northeast, West Coast)")

    return dim_location


def create_dim_employment_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the employment type dimension table.

    Args:
        df: Cleaned job postings DataFrame

    Returns:
        pd.DataFrame: Employment type dimension table
    """
    print("\nCreating dim_employment_type...")

    dim_employment_type = pd.DataFrame({
        'employment_type_id': [1, 2, 3],
        'employment_type': ['Full-time', 'Contract', 'Part-time'],
        'work_arrangement': ['Remote', 'Hybrid', 'On-site']
    })

    print(f"  Created {len(dim_employment_type):,} unique employment type records")
    print("  TODO: Extract unique combinations from source data")

    return dim_employment_type


def create_fact_posting_base(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the base fact table with cleaned data.

    Args:
        df: Cleaned job postings DataFrame

    Returns:
        pd.DataFrame: Fact table base
    """
    print("\nCreating fact_posting base...")

    # TODO: Select relevant columns and assign foreign keys
    fact_columns = ['salary_min', 'salary_max', 'salary_currency']

    fact_posting = df[fact_columns].copy() if all(col in df.columns for col in fact_columns) else pd.DataFrame()

    # Add surrogate key
    if len(fact_posting) > 0:
        fact_posting.insert(0, 'posting_id', range(1, len(fact_posting) + 1))
    else:
        fact_posting = pd.DataFrame(columns=['posting_id'] + fact_columns)

    print(f"  Created fact table base with {len(fact_posting):,} records")
    print("  TODO: Add foreign keys to dimension tables")
    print("  TODO: Add posted_date column")
    print("  TODO: Add application_url if available")

    return fact_posting


def save_outputs(dim_job, dim_company, dim_location, dim_employment_type,
                 dim_skill, bridge_posting_skill, fact_posting, output_dir: Path):
    """
    Save all dimension tables and fact table to CSV files.

    Args:
        dim_*: Dimension DataFrames
        bridge_posting_skill: Bridge table DataFrame
        fact_posting: Fact table DataFrame
        output_dir: Directory where to save files
    """
    print("\nSaving dimension tables and fact table...")

    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        'dim_job.csv': dim_job,
        'dim_company.csv': dim_company,
        'dim_location.csv': dim_location,
        'dim_employment_type.csv': dim_employment_type,
        'dim_skill.csv': dim_skill,
        'bridge_posting_skill.csv': bridge_posting_skill,
        'job_postings_cleaned.csv': fact_posting,
    }

    for filename, df in outputs.items():
        filepath = output_dir / filename
        df.to_csv(filepath, index=False)
        print(f"  ✓ Saved {filename} ({len(df):,} rows)")


def main():
    """Main execution flow."""
    print("="*70)
    print("JOB MARKET ANALYTICS - STEP 2: CLEAN AND NORMALIZE")
    print("="*70)

    paths = setup_paths()

    # Load the combined raw data
    print(f"\nLoading data from: {paths['input_csv']}")
    try:
        df = pd.read_csv(paths['input_csv'])
        print(f"✓ Loaded {len(df):,} rows")
    except FileNotFoundError:
        print(f"ERROR: Input file not found. Please run 01_ingest_raw_files.py first.")
        sys.exit(1)

    # Data cleaning and normalization
    df = normalize_column_names(df)
    df = clean_job_postings(df)
    df = parse_salary(df)
    df = standardize_locations(df)
    df = normalize_employment_type(df)
    df = derive_seniority_level(df)
    df = categorize_job_title(df)

    # Extract skills
    bridge_posting_skill, dim_skill = extract_skills(df)

    # Create dimension tables
    dim_job = create_dim_job(df)
    dim_company = create_dim_company(df)
    dim_location = create_dim_location(df)
    dim_employment_type = create_dim_employment_type(df)

    # Create fact table base
    fact_posting = create_fact_posting_base(df)

    # Save all outputs
    save_outputs(dim_job, dim_company, dim_location, dim_employment_type,
                 dim_skill, bridge_posting_skill, fact_posting, paths['output_dir'])

    print("\n" + "="*70)
    print("STEP 2 COMPLETE: Data cleaned and dimensional tables created")
    print(f"Next step: Run python/03_export_for_sql_load.py")
    print("="*70)

    # TODO: Add data quality report generation
    # TODO: Add validation that all foreign keys will join properly
    # TODO: Add summary statistics for each dimension


if __name__ == "__main__":
    main()
