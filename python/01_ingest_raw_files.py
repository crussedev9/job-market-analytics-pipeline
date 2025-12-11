"""
Job Market Analytics Pipeline - Step 1: Ingest Raw Files

This script reads the raw job postings CSV file from Kaggle and performs initial
validation and ingestion. It outputs a combined raw file to the interim folder
for further processing.

Author: Analytics Portfolio Project
"""

import pandas as pd
from pathlib import Path
import sys


def setup_paths() -> dict:
    """
    Set up project paths for cross-platform compatibility.

    Returns:
        dict: Dictionary containing project paths
    """
    # Get project root (assuming script is in project/python/)
    project_root = Path(__file__).parent.parent

    paths = {
        'raw_data': project_root / 'data' / 'raw',
        'interim_data': project_root / 'data' / 'interim',
        'raw_csv': project_root / 'data' / 'raw' / 'job_postings_raw.csv',
        'output_csv': project_root / 'data' / 'interim' / 'job_postings_raw_combined.csv'
    }

    return paths


def validate_raw_file(file_path: Path) -> bool:
    """
    Check if the raw data file exists and is readable.

    Args:
        file_path: Path to the raw CSV file

    Returns:
        bool: True if file exists and is valid, False otherwise
    """
    if not file_path.exists():
        print(f"ERROR: Raw data file not found at: {file_path}")
        print("Please download the Kaggle job postings dataset and place it in data/raw/")
        return False

    if file_path.stat().st_size == 0:
        print(f"ERROR: Raw data file is empty: {file_path}")
        return False

    print(f"✓ Found raw data file: {file_path}")
    return True


def ingest_raw_csv(file_path: Path) -> pd.DataFrame:
    """
    Read the raw CSV file into a pandas DataFrame.

    Args:
        file_path: Path to the raw CSV file

    Returns:
        pd.DataFrame: Loaded data
    """
    print(f"\nReading raw CSV file...")

    # TODO: Add error handling for different CSV encodings (utf-8, latin1, etc.)
    # TODO: Add parameter to handle different delimiters if needed

    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(f"✓ Successfully loaded {len(df):,} rows")
        return df

    except Exception as e:
        print(f"ERROR: Failed to read CSV file: {e}")
        sys.exit(1)


def display_data_info(df: pd.DataFrame) -> None:
    """
    Display summary information about the loaded dataset.

    Args:
        df: DataFrame to analyze
    """
    print("\n" + "="*70)
    print("RAW DATA SUMMARY")
    print("="*70)

    print(f"\nDataset Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

    print(f"\nColumn Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")

    print(f"\nData Types:")
    print(df.dtypes)

    print(f"\nNull Value Counts:")
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df) * 100).round(2)
    null_summary = pd.DataFrame({
        'Column': null_counts.index,
        'Null_Count': null_counts.values,
        'Null_Percentage': null_pct.values
    })
    print(null_summary[null_summary['Null_Count'] > 0].to_string(index=False))

    print(f"\nMemory Usage:")
    print(f"  {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    print("\n" + "="*70)

    # TODO: Add schema validation against expected columns
    # Expected columns: job_id, title, company, location, salary, skills, etc.
    # TODO: Add data quality checks (e.g., check for completely empty rows)


def save_to_interim(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save the raw data to the interim folder for next processing step.

    Args:
        df: DataFrame to save
        output_path: Path where to save the CSV
    """
    print(f"\nSaving to interim folder...")

    # Ensure interim directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        df.to_csv(output_path, index=False)
        print(f"✓ Saved combined raw data to: {output_path}")
        print(f"  File size: {output_path.stat().st_size / 1024**2:.2f} MB")

    except Exception as e:
        print(f"ERROR: Failed to save interim file: {e}")
        sys.exit(1)


def main():
    """
    Main execution flow for raw data ingestion.
    """
    print("="*70)
    print("JOB MARKET ANALYTICS - STEP 1: INGEST RAW FILES")
    print("="*70)

    # Setup paths
    paths = setup_paths()

    # Validate raw file exists
    if not validate_raw_file(paths['raw_csv']):
        sys.exit(1)

    # Load raw data
    df_raw = ingest_raw_csv(paths['raw_csv'])

    # Display summary information
    display_data_info(df_raw)

    # Save to interim folder
    save_to_interim(df_raw, paths['output_csv'])

    print("\n" + "="*70)
    print("STEP 1 COMPLETE: Raw data ingested successfully")
    print(f"Next step: Run python/02_clean_and_normalize.py")
    print("="*70)

    # TODO: Add support for multiple raw CSV files (batch processing)
    # TODO: Add logging to file instead of just print statements
    # TODO: Add command-line arguments for custom file paths
    # TODO: Add data profiling report generation (optional)


if __name__ == "__main__":
    main()
