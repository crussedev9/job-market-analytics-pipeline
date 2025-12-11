"""
Create a 10% sample of the Glassdoor dataset for faster testing.

This creates a sample with ~16,500 rows instead of 165,000 for quick testing.
"""

import pandas as pd
from pathlib import Path

# Paths
raw_dir = Path(__file__).parent / 'data' / 'raw'
full_file = raw_dir / 'job_postings_raw.csv'
backup_file = raw_dir / 'job_postings_raw_FULL.csv'
sample_file = raw_dir / 'job_postings_raw_SAMPLE.csv'

print("="*70)
print("CREATING SAMPLE DATASET (10% of full data)")
print("="*70)

# Check if full file exists
if not full_file.exists():
    print(f"ERROR: {full_file} not found!")
    print("Make sure you've copied glassdoor.csv to this location.")
    exit(1)

print(f"\n1. Loading full dataset from {full_file.name}...")
df_full = pd.read_csv(full_file)
print(f"   ✓ Loaded {len(df_full):,} rows")

# Create backup if it doesn't exist
if not backup_file.exists():
    print(f"\n2. Creating backup: {backup_file.name}...")
    df_full.to_csv(backup_file, index=False)
    print(f"   ✓ Backup created")
else:
    print(f"\n2. Backup already exists: {backup_file.name}")

# Create 10% sample
print(f"\n3. Creating 10% random sample...")
df_sample = df_full.sample(frac=0.10, random_state=42)
print(f"   ✓ Sample created: {len(df_sample):,} rows")

# Save sample
print(f"\n4. Saving sample: {sample_file.name}...")
df_sample.to_csv(sample_file, index=False)
print(f"   ✓ Sample saved")

# Replace original with sample
print(f"\n5. Replacing {full_file.name} with sample...")
df_sample.to_csv(full_file, index=False)
print(f"   ✓ Done! {full_file.name} now contains {len(df_sample):,} rows")

print("\n" + "="*70)
print("SAMPLE CREATED SUCCESSFULLY")
print("="*70)
print(f"\nFiles created:")
print(f"  - {backup_file.name} - Full dataset ({len(df_full):,} rows) [BACKUP]")
print(f"  - {sample_file.name} - Sample dataset ({len(df_sample):,} rows) [SAVED]")
print(f"  - {full_file.name} - Now contains sample ({len(df_sample):,} rows) [ACTIVE]")
print(f"\nYou can now run the pipeline:")
print(f"  python python/01_ingest_raw_files.py")
print(f"  python python/02_clean_and_normalize_glassdoor.py")
print(f"  python python/03_export_for_sql_load.py")
print(f"\nTo restore the full dataset later:")
print(f"  copy data\\raw\\job_postings_raw_FULL.csv data\\raw\\job_postings_raw.csv")
print("="*70)
