# Job Market Analytics Pipeline

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A professional end-to-end ETL and analytics project demonstrating data engineering and business intelligence skills for Analytics Engineer and Senior BI Analyst roles.

## Overview

This project ingests raw job posting data from Kaggle, transforms it through Python and SQL into a dimensional model, and prepares analytics-ready tables for a Power BI dashboard. The pipeline explores job market trends including skills in demand, salary ranges, and remote vs on-site work patterns for data and analytics roles.

## Tech Stack

- **Language:** Python 3.8+
- **Libraries:** pandas, sqlalchemy
- **Database:** SQLite
- **Data Modeling:** Star schema (dimensional modeling)
- **Transformation:** SQL (CTEs, joins, analytical views)
- **BI Preparation:** Power Query (M language)
- **Visualization:** Power BI (planned)
- **Version Control:** Git/GitHub

## Architecture

```
Raw CSV (Kaggle)
    ↓
[Python Ingestion & Cleaning]
    ↓
[SQLite Dimensional Model]
    ↓
[SQL Analytical Views]
    ↓
[Power Query Transformations]
    ↓
[Power BI Dashboard]
```

## Dimensional Model

The pipeline implements a **star schema** optimized for analytical queries:

### Fact Table
- **fact_posting** - One row per job posting (grain: individual posting)

### Dimension Tables
- **dim_job** - Job titles, categories, seniority levels
- **dim_company** - Company names, industries, sizes
- **dim_location** - Cities, states, countries, regions
- **dim_employment_type** - Full-time/Contract, Remote/Hybrid/On-site
- **dim_skill** - Skills and skill categories

### Bridge Table
- **bridge_posting_skill** - Many-to-many relationship between postings and skills

## Business Questions

This pipeline is designed to answer key questions about the analytics job market:

- **Which skills are most in demand for analytics roles?**
- **How do salary ranges vary by job title and location?**
- **What is the trend for remote vs on-site roles?**
- **Which locations have the highest concentration of analytics jobs?**
- **What is the relationship between seniority level and compensation?**
- **Which skills correlate with higher salaries?**

## Project Structure

```
job-market-analytics-pipeline/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── data/
│   ├── raw/                          # Original Kaggle CSV (user-supplied)
│   ├── interim/                      # Intermediate cleaned CSVs
│   └── processed/                    # Analytics-ready tables
├── python/
│   ├── 01_ingest_raw_files.py       # Read and validate raw data
│   ├── 02_clean_and_normalize.py    # Clean and prepare dimensions
│   └── 03_export_for_sql_load.py    # Load into SQLite
├── sql/
│   ├── create_tables.sql            # Dimensional model DDL
│   ├── staging_transforms.sql       # Transform staging to star schema
│   └── analytics_views.sql          # Business-focused analytical views
├── power_query/
│   └── job_postings_power_query_m_code.txt  # M code for Power BI
├── bi/
│   └── README_bi_layer.md           # Power BI dashboard design
└── docs/
    ├── data_model.md                # Dimensional model documentation
    ├── pipeline_design.md           # Pipeline architecture details
    └── dashboard_design.md          # Dashboard wireframes and specs
```

## Setup and Usage

### Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Power BI Desktop for visualization

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd job-market-analytics-pipeline
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Add your Kaggle job postings CSV to `data/raw/`:
```bash
# Download your dataset and place it in data/raw/
# Expected filename: job_postings_raw.csv
```

### Running the Pipeline

Execute the Python scripts in order:

```bash
# Step 1: Ingest raw data
python python/01_ingest_raw_files.py

# Step 2: Clean and normalize data
python python/02_clean_and_normalize.py

# Step 3: Load into SQLite and create dimensional model
python python/03_export_for_sql_load.py

# Step 4: Execute SQL transformations
# (Run SQL scripts in your SQLite client or via Python)

# Step 5: Connect Power BI to the processed data
# (Use Power Query M code from power_query/ folder)
```

## Data Source

This project uses job postings data from Kaggle. The raw CSV file should contain columns such as:
- Job ID, Title, Company
- Location (City, State, Country)
- Salary range
- Skills/Requirements
- Employment type (Full-time, Contract, etc.)
- Work arrangement (Remote, Hybrid, On-site)
- Posted date

**Note:** The raw data file is not included in this repository. Add your own dataset to `data/raw/` before running the pipeline.

## Key Features

- **Professional ETL Design:** Clear separation of ingestion, transformation, and analytical layers
- **Dimensional Modeling:** Star schema optimized for BI tools and analytical queries
- **Data Quality:** Normalization and standardization of locations, salaries, and employment types
- **Skill Extraction:** Parsing and categorization of technical skills from job descriptions
- **Analytical Views:** Pre-built SQL views answering common business questions
- **Power BI Ready:** Structured data model and Power Query templates for dashboard creation
- **Well-Documented:** Comprehensive documentation of design decisions and pipeline flow

## Future Enhancements

- Add incremental data loading for new job postings
- Implement data quality checks and validation rules
- Create automated testing for transformations
- Build interactive Power BI dashboard (.pbix file)
- Add more sophisticated skill extraction using NLP
- Include time-series analysis for trend detection
- Expand to multiple job boards beyond Kaggle dataset

## Documentation

For detailed information, see the `docs/` folder:
- [Data Model Documentation](docs/data_model.md) - Star schema design and relationships
- [Pipeline Design](docs/pipeline_design.md) - End-to-end architecture and data flow
- [Dashboard Design](docs/dashboard_design.md) - Planned Power BI dashboard specifications

## Skills Demonstrated

This project showcases:
- **Data Engineering:** ETL pipeline design, data ingestion, transformation
- **SQL & Data Modeling:** Dimensional modeling, star schema, analytical queries
- **Python:** pandas for data manipulation, SQLAlchemy for database interaction
- **Business Intelligence:** Power Query, dashboard design, KPI definition
- **Analytics:** Trend analysis, salary benchmarking, skill demand analysis
- **Documentation:** Clear technical writing, design documentation, user guides
- **Version Control:** Git workflow, commit hygiene, professional repository structure

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**crussedev9**

Created as a portfolio project to demonstrate Analytics Engineer / Senior BI Analyst capabilities.

- GitHub: [@crussedev9](https://github.com/crussedev9)
- Project Link: [https://github.com/crussedev9/job-market-analytics-pipeline](https://github.com/crussedev9/job-market-analytics-pipeline)

---

⭐ If you find this project helpful or interesting, please consider giving it a star!
