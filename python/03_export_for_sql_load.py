"""
Job Market Analytics Pipeline - Step 3: Export for SQL Load

This script loads the cleaned dimensional data into a SQLite database.
It creates staging tables and loads the CSV data, preparing it for
SQL transformation into the final star schema.

Author: Analytics Portfolio Project
"""

import pandas as pd
from pathlib import Path
import sqlite3
import sys


def setup_paths() -> dict:
    """Set up project paths."""
    project_root = Path(__file__).parent.parent

    paths = {
        'interim_dir': project_root / 'data' / 'interim',
        'processed_dir': project_root / 'data' / 'processed',
        'db_path': project_root / 'job_market.db',
    }

    return paths


def get_interim_files(interim_dir: Path) -> dict:
    """
    Get all interim CSV files for loading.

    Args:
        interim_dir: Path to interim data directory

    Returns:
        dict: Dictionary mapping table names to file paths
    """
    files = {
        'stg_dim_job': interim_dir / 'dim_job.csv',
        'stg_dim_company': interim_dir / 'dim_company.csv',
        'stg_dim_location': interim_dir / 'dim_location.csv',
        'stg_dim_employment_type': interim_dir / 'dim_employment_type.csv',
        'stg_dim_skill': interim_dir / 'dim_skill.csv',
        'stg_bridge_posting_skill': interim_dir / 'bridge_posting_skill.csv',
        'stg_fact_posting': interim_dir / 'job_postings_cleaned.csv',
    }

    return files


def create_sqlite_connection(db_path: Path) -> sqlite3.Connection:
    """
    Create a connection to the SQLite database.

    Args:
        db_path: Path to SQLite database file

    Returns:
        sqlite3.Connection: Database connection
    """
    print(f"\nConnecting to SQLite database: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        print(f"✓ Connected to database")
        return conn

    except Exception as e:
        print(f"ERROR: Failed to connect to database: {e}")
        sys.exit(1)


def load_csv_to_staging(conn: sqlite3.Connection, table_name: str,
                        csv_path: Path) -> int:
    """
    Load a CSV file into a SQLite staging table.

    Args:
        conn: SQLite database connection
        table_name: Name of the staging table
        csv_path: Path to the CSV file

    Returns:
        int: Number of rows loaded
    """
    try:
        # Read CSV
        df = pd.read_csv(csv_path)

        # Load into SQLite (replace if exists)
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"  ✓ Loaded {len(df):,} rows into {table_name}")
        return len(df)

    except FileNotFoundError:
        print(f"  ⚠ File not found: {csv_path} - Skipping")
        return 0
    except Exception as e:
        print(f"  ERROR loading {table_name}: {e}")
        return 0


def export_to_processed_folder(conn: sqlite3.Connection, processed_dir: Path):
    """
    Export tables from SQLite to processed folder as CSV files.
    This is an alternative approach for Power BI connectivity.

    Args:
        conn: SQLite database connection
        processed_dir: Path to processed data directory
    """
    print("\nExporting tables to processed folder (optional)...")

    # TODO: After SQL transformations are complete, export final tables
    # tables_to_export = [
    #     'fact_posting',
    #     'dim_job',
    #     'dim_company',
    #     'dim_location',
    #     'dim_employment_type',
    #     'dim_skill',
    #     'bridge_posting_skill'
    # ]

    processed_dir.mkdir(parents=True, exist_ok=True)

    print("  TODO: Implement export of final dimensional tables to CSV")
    print("  TODO: This step runs after SQL transformations complete")
    print(f"  TODO: Export destination: {processed_dir}")

    # Example export code (uncomment when ready):
    # for table in tables_to_export:
    #     query = f"SELECT * FROM {table}"
    #     df = pd.read_sql_query(query, conn)
    #     output_path = processed_dir / f"{table}.csv"
    #     df.to_csv(output_path, index=False)
    #     print(f"  ✓ Exported {table} ({len(df):,} rows)")


def execute_sql_script(conn: sqlite3.Connection, script_path: Path) -> None:
    """
    Execute a SQL script file.

    Args:
        conn: SQLite database connection
        script_path: Path to SQL script file
    """
    print(f"\nExecuting SQL script: {script_path.name}")

    try:
        with open(script_path, 'r') as f:
            sql_script = f.read()

        conn.executescript(sql_script)
        conn.commit()
        print(f"  ✓ Successfully executed {script_path.name}")

    except FileNotFoundError:
        print(f"  ⚠ SQL script not found: {script_path}")
    except Exception as e:
        print(f"  ERROR executing SQL script: {e}")


def display_database_summary(conn: sqlite3.Connection):
    """
    Display summary information about the database.

    Args:
        conn: SQLite database connection
    """
    print("\n" + "="*70)
    print("DATABASE SUMMARY")
    print("="*70)

    # Get list of tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()

    print(f"\nTables in database: {len(tables)}")

    for (table_name,) in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"  - {table_name}: {row_count:,} rows")

    print("\n" + "="*70)


def main():
    """Main execution flow."""
    print("="*70)
    print("JOB MARKET ANALYTICS - STEP 3: EXPORT FOR SQL LOAD")
    print("="*70)

    paths = setup_paths()

    # Create database connection
    conn = create_sqlite_connection(paths['db_path'])

    # Get interim CSV files
    interim_files = get_interim_files(paths['interim_dir'])

    # Load all CSV files into staging tables
    print("\nLoading CSV files into SQLite staging tables...")
    total_rows = 0

    for table_name, csv_path in interim_files.items():
        rows_loaded = load_csv_to_staging(conn, table_name, csv_path)
        total_rows += rows_loaded

    print(f"\n✓ Total rows loaded across all tables: {total_rows:,}")

    # Display database summary
    display_database_summary(conn)

    # TODO: Execute SQL transformation scripts
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. Execute SQL scripts to create dimensional model:")
    print("   - Run sql/create_tables.sql to create final schema")
    print("   - Run sql/staging_transforms.sql to populate dimensions and fact table")
    print("   - Run sql/analytics_views.sql to create analytical views")
    print("\n2. Options for executing SQL:")
    print("   Option A: Use a SQLite GUI tool (DB Browser for SQLite)")
    print("   Option B: Uncomment and use execute_sql_script() function below")
    print("   Option C: Run via command line: sqlite3 job_market.db < sql/create_tables.sql")
    print("\n3. Connect Power BI to the database or export to CSV")

    # Uncomment these lines when SQL scripts are ready:
    # project_root = Path(__file__).parent.parent
    # execute_sql_script(conn, project_root / 'sql' / 'create_tables.sql')
    # execute_sql_script(conn, project_root / 'sql' / 'staging_transforms.sql')
    # execute_sql_script(conn, project_root / 'sql' / 'analytics_views.sql')

    # Optional: Export to processed folder
    # export_to_processed_folder(conn, paths['processed_dir'])

    # Close connection
    conn.close()
    print("\n" + "="*70)
    print("STEP 3 COMPLETE: Data loaded into SQLite database")
    print(f"Database location: {paths['db_path']}")
    print("="*70)

    # TODO: Add option to export final tables to data/processed/ folder
    # TODO: Add data quality checks after SQL transformations
    # TODO: Add automatic execution of SQL scripts


if __name__ == "__main__":
    main()
