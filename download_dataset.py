"""
Download Kaggle Dataset - Data Science Job Postings

Prerequisites:
1. Install kaggle package: pip install kaggle
2. Set up Kaggle API credentials:
   - Go to https://www.kaggle.com/account
   - Click "Create New API Token"
   - Save kaggle.json to C:\Users\<username>\.kaggle\kaggle.json

Usage:
    python download_dataset.py
"""

import os
from pathlib import Path
import zipfile

def download_kaggle_dataset():
    """Download the Glassdoor Data Science jobs dataset from Kaggle."""

    # Project paths
    project_root = Path(__file__).parent
    raw_data_dir = project_root / 'data' / 'raw'
    raw_data_dir.mkdir(parents=True, exist_ok=True)

    # Kaggle dataset identifier
    dataset = "andresionek/data-science-job-postings-on-glassdoor"

    print("Downloading dataset from Kaggle...")
    print(f"Dataset: {dataset}")

    try:
        # Download using Kaggle API
        import kaggle

        kaggle.api.dataset_download_files(
            dataset,
            path=raw_data_dir,
            unzip=True
        )

        print(f"✓ Dataset downloaded to: {raw_data_dir}")

        # List downloaded files
        print("\nDownloaded files:")
        for file in raw_data_dir.glob("*.csv"):
            print(f"  - {file.name}")

        # Try to find and rename the main file
        csv_files = list(raw_data_dir.glob("*.csv"))

        if csv_files:
            main_file = csv_files[0]  # Assume first CSV is the main one
            target_file = raw_data_dir / "job_postings_raw.csv"

            if main_file.name != "job_postings_raw.csv":
                print(f"\nRenaming {main_file.name} → job_postings_raw.csv")
                main_file.rename(target_file)

            print(f"\n✓ Ready to run ETL pipeline!")
            print(f"   Run: python python/01_ingest_raw_files.py")

    except ImportError:
        print("ERROR: kaggle package not installed.")
        print("Install with: pip install kaggle")
        print("\nAlternatively, download manually from:")
        print(f"https://www.kaggle.com/datasets/{dataset}")

    except Exception as e:
        print(f"ERROR: {e}")
        print("\nManual download instructions:")
        print(f"1. Go to: https://www.kaggle.com/datasets/{dataset}")
        print(f"2. Click 'Download'")
        print(f"3. Extract ZIP and place CSV in: {raw_data_dir}")
        print(f"4. Rename to: job_postings_raw.csv")


if __name__ == "__main__":
    download_kaggle_dataset()
