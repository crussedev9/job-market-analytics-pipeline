# Data Model Documentation

## Overview

The Job Market Analytics Pipeline implements a **star schema** dimensional model optimized for analytical queries and Business Intelligence reporting. This design follows Kimball methodology for dimensional modeling.

---

## Schema Type: Star Schema

A star schema consists of:
- **One central fact table** containing measurements and foreign keys
- **Multiple dimension tables** containing descriptive attributes
- **One bridge table** to handle many-to-many relationships

This design optimizes query performance and simplifies reporting in BI tools like Power BI.

---

## Entity Relationship Diagram (Text Format)

```
                    dim_job
                        |
                        | job_id
                        |
    dim_company --------|
        |               |
        | company_id    |
        |               |
        +---> fact_posting <----+
                |               |
                | location_id   | employment_type_id
                |               |
           dim_location    dim_employment_type


    dim_skill <---> bridge_posting_skill <---> fact_posting
    (many-to-many relationship via bridge table)
```

---

## Fact Table

### fact_posting

**Purpose:** Store measurable facts about each job posting

**Grain:** One row per job posting (each posting is uniquely identified)

**Type:** Transaction fact table

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `posting_id` | INTEGER (PK) | Unique identifier for posting | 12345 |
| `job_id` | INTEGER (FK) | Foreign key to dim_job | 101 |
| `company_id` | INTEGER (FK) | Foreign key to dim_company | 201 |
| `location_id` | INTEGER (FK) | Foreign key to dim_location | 301 |
| `employment_type_id` | INTEGER (FK) | Foreign key to dim_employment_type | 401 |
| `posted_date` | DATE | Date posting was published | 2024-03-15 |
| `salary_min` | DECIMAL(10,2) | Minimum salary in range | 80000.00 |
| `salary_max` | DECIMAL(10,2) | Maximum salary in range | 120000.00 |
| `salary_currency` | VARCHAR(10) | Currency code | USD |
| `application_url` | VARCHAR(500) | Link to apply | https://... |

**Key Measures:**
- Count of postings
- Average salary (calculated from min/max)
- Salary range width

---

## Dimension Tables

### dim_job

**Purpose:** Describe job characteristics

**Type:** Type 1 SCD (Slowly Changing Dimension - overwrite)

**Hierarchy:** Job Category → Seniority Level → Job Title

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `job_id` | INTEGER (PK) | Surrogate key | 101 |
| `job_title` | VARCHAR(255) | Full job title | Senior Data Analyst |
| `job_category` | VARCHAR(100) | Broad category | Data Analytics |
| `seniority_level` | VARCHAR(50) | Level of seniority | Senior |

**Sample Values:**
- **job_category:** Data Analytics, Data Science, Data Engineering, Business Intelligence, Other
- **seniority_level:** Junior, Mid-level, Senior, Lead, Principal, Director, VP, C-Level

---

### dim_company

**Purpose:** Describe companies posting jobs

**Type:** Type 1 SCD

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `company_id` | INTEGER (PK) | Surrogate key | 201 |
| `company_name` | VARCHAR(255) | Name of company | Acme Analytics Corp |
| `industry` | VARCHAR(100) | Industry classification | Technology |
| `company_size` | VARCHAR(50) | Employee count range | 201-1000 |

**Sample Values:**
- **industry:** Technology, Finance, Healthcare, Retail, Consulting, Government, Education
- **company_size:** 1-50, 51-200, 201-1000, 1001-5000, 5000+

---

### dim_location

**Purpose:** Describe geographic locations

**Type:** Type 1 SCD

**Hierarchy:** Country → Region → State → City

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `location_id` | INTEGER (PK) | Surrogate key | 301 |
| `city` | VARCHAR(100) | City name | San Francisco |
| `state` | VARCHAR(50) | State/province | CA |
| `country` | VARCHAR(100) | Country | USA |
| `region` | VARCHAR(50) | Geographic region | West Coast |
| `is_remote` | BOOLEAN | True if fully remote | 0 (False) |

**Sample Values:**
- **region:** Northeast, Southeast, Midwest, West Coast, Southwest, International
- **is_remote:** 1 (True) for "Remote", 0 (False) for physical locations

**Special Case:** Remote positions have:
- `city` = "Remote"
- `state` = NULL
- `is_remote` = 1

---

### dim_employment_type

**Purpose:** Describe employment characteristics

**Type:** Type 1 SCD

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `employment_type_id` | INTEGER (PK) | Surrogate key | 401 |
| `employment_type` | VARCHAR(50) | Employment classification | Full-time |
| `work_arrangement` | VARCHAR(50) | Where work is performed | Remote |

**Sample Values:**
- **employment_type:** Full-time, Contract, Part-time, Temporary, Internship
- **work_arrangement:** Remote, Hybrid, On-site

**Note:** This dimension captures the combination of employment type and work arrangement, allowing analysis like "Full-time Remote vs Full-time Hybrid"

---

### dim_skill

**Purpose:** Catalog technical and professional skills

**Type:** Type 1 SCD

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `skill_id` | INTEGER (PK) | Surrogate key | 501 |
| `skill_name` | VARCHAR(100) | Skill name | SQL |
| `skill_category` | VARCHAR(100) | Skill grouping | Databases |

**Sample Values:**
- **skill_category:**
  - Programming (Python, R, Java, JavaScript)
  - Databases (SQL, PostgreSQL, MongoDB)
  - BI Tools (Power BI, Tableau, Looker, Qlik)
  - Cloud (AWS, Azure, GCP)
  - Data Engineering (Airflow, Spark, Kafka)
  - Analytics (Excel, Statistics, A/B Testing)

---

## Bridge Table (Many-to-Many Resolution)

### bridge_posting_skill

**Purpose:** Resolve many-to-many relationship between postings and skills

A single job posting can require multiple skills, and a single skill appears in multiple postings.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `posting_id` | INTEGER (PK, FK) | Foreign key to fact_posting | 12345 |
| `skill_id` | INTEGER (PK, FK) | Foreign key to dim_skill | 501 |

**Composite Primary Key:** (posting_id, skill_id)

**Grain:** One row per posting-skill combination

**Example:**
Posting #12345 (Senior Data Analyst) requires Python, SQL, and Power BI:
```
posting_id | skill_id
-----------|---------
12345      | 501      (SQL)
12345      | 502      (Python)
12345      | 503      (Power BI)
```

---

## Relationships

### One-to-Many Relationships

All relationships from fact to dimensions are **many-to-one** (from the fact table perspective):

1. **fact_posting → dim_job**
   - Cardinality: Many-to-One
   - Many postings can have the same job title

2. **fact_posting → dim_company**
   - Cardinality: Many-to-One
   - Many postings can be from the same company

3. **fact_posting → dim_location**
   - Cardinality: Many-to-One
   - Many postings can be in the same location

4. **fact_posting → dim_employment_type**
   - Cardinality: Many-to-One
   - Many postings can have the same employment type

### Many-to-Many Relationship

5. **fact_posting ↔ dim_skill** (via bridge_posting_skill)
   - Cardinality: Many-to-Many
   - One posting requires many skills
   - One skill is required by many postings
   - Resolved via bridge table

---

## Design Decisions

### Why Star Schema?

1. **Query Performance:** Denormalized dimensions mean fewer joins
2. **BI Tool Compatibility:** Most BI tools optimize for star schemas
3. **User-Friendly:** Business users can easily understand the model
4. **Aggregation Speed:** Pre-joined dimensions accelerate GROUP BY queries

### Why Separate dim_employment_type?

- Facilitates analysis of remote vs on-site trends
- Allows filtering by work arrangement independently of job title
- Enables tracking of employment type shifts over time

### Why Bridge Table for Skills?

- A posting can require 5+ skills (many-to-many relationship)
- Allows skill demand analysis: "How many postings require Python?"
- Enables skill co-occurrence analysis: "What skills appear together?"
- Alternative (storing skills as comma-separated in fact table) would be inefficient for querying

### Why Type 1 SCD for All Dimensions?

- This is a **snapshot** model for job market analysis
- Historical changes to company names, job titles, etc., are not critical
- Simplifies implementation for a portfolio project
- In production, some dimensions (e.g., company) might use Type 2 to track history

---

## Slowly Changing Dimensions (SCD)

All dimensions use **Type 1 SCD**: Overwrite changes

- **Pros:** Simple, no historical tracking needed
- **Cons:** Lose history if a company changes name or industry

**Future Enhancement:** Implement Type 2 SCD for dim_company to track company growth (size changes) over time.

---

## Data Refresh Strategy

### For Portfolio/Demo Use:
- **Full Refresh:** Replace all data when new Kaggle dataset is downloaded
- **Frequency:** On-demand (when user re-runs ETL pipeline)

### For Production Use (Hypothetical):
- **Incremental Load:** Only load new postings since last refresh
- **Dimensions:** Upsert (insert new, update existing)
- **Fact Table:** Append new postings, potentially update if postings are edited
- **Frequency:** Daily refresh (nightly batch job)

---

## Data Quality Constraints

### Referential Integrity
- All foreign keys in fact_posting must exist in dimension tables
- Enforced via foreign key constraints in create_tables.sql

### Business Rules
1. **Salary Range:** salary_min ≤ salary_max
2. **Posted Date:** Must be a valid date, typically <= today
3. **Mandatory Fields:**
   - fact_posting: posting_id, job_id, company_id
   - dim_skill: skill_name (no duplicates)
   - dim_company: company_name

### Data Quality Checks
- See staging_transforms.sql for orphaned record checks
- TODO: Implement data quality dashboard showing % nulls, outliers, etc.

---

## Metrics and Calculations

### Core Metrics
- **Posting Count:** `COUNT(posting_id)`
- **Average Salary:** `AVG((salary_min + salary_max) / 2)`
- **Median Salary:** `MEDIAN((salary_min + salary_max) / 2)`

### Derived Metrics (Calculated in SQL Views or Power BI)
- **Salary Midpoint:** `(salary_min + salary_max) / 2`
- **Salary Range Width:** `salary_max - salary_min`
- **% Remote Positions:** `COUNT(CASE WHEN is_remote=1) / COUNT(*)`
- **Skills per Posting:** `COUNT(skill_id) GROUP BY posting_id`
- **Postings per Skill:** `COUNT(posting_id) GROUP BY skill_id`

---

## SQL Query Examples

### Simple Aggregation: Postings by Job Category
```sql
SELECT
    j.job_category,
    COUNT(f.posting_id) AS posting_count,
    ROUND(AVG((f.salary_min + f.salary_max) / 2.0), 2) AS avg_salary
FROM fact_posting f
JOIN dim_job j ON f.job_id = j.job_id
GROUP BY j.job_category
ORDER BY posting_count DESC;
```

### Multi-Dimension Analysis: Salary by Location and Seniority
```sql
SELECT
    l.state,
    j.seniority_level,
    COUNT(f.posting_id) AS posting_count,
    ROUND(AVG((f.salary_min + f.salary_max) / 2.0), 2) AS avg_salary
FROM fact_posting f
JOIN dim_job j ON f.job_id = j.job_id
JOIN dim_location l ON f.location_id = l.location_id
WHERE l.state IS NOT NULL
GROUP BY l.state, j.seniority_level
HAVING posting_count >= 5
ORDER BY l.state, avg_salary DESC;
```

### Bridge Table Query: Top Skills
```sql
SELECT
    s.skill_name,
    s.skill_category,
    COUNT(DISTINCT b.posting_id) AS posting_count
FROM dim_skill s
JOIN bridge_posting_skill b ON s.skill_id = b.skill_id
GROUP BY s.skill_name, s.skill_category
ORDER BY posting_count DESC
LIMIT 20;
```

---

## Model Statistics (Example)

These are placeholder statistics - actual values will depend on the Kaggle dataset:

| Table Name | Est. Row Count | Growth Rate |
|-----------|---------------|-------------|
| fact_posting | 10,000 - 100,000 | Grows with each data refresh |
| dim_job | 500 - 2,000 | Slow growth (new job titles) |
| dim_company | 1,000 - 5,000 | Medium growth (new companies) |
| dim_location | 200 - 1,000 | Slow growth (new cities) |
| dim_employment_type | 10 - 30 | Minimal growth (fixed combinations) |
| dim_skill | 50 - 200 | Slow growth (new skills/technologies) |
| bridge_posting_skill | 50,000 - 500,000 | Grows with postings (5-10 skills per posting) |

---

## Power BI Model Configuration

### Relationships in Power BI

When using CSV import (not SQLite views):

1. Create relationships in Model view:
   - fact_posting[job_id] → dim_job[job_id] (Many-to-One)
   - fact_posting[company_id] → dim_company[company_id] (Many-to-One)
   - fact_posting[location_id] → dim_location[location_id] (Many-to-One)
   - fact_posting[employment_type_id] → dim_employment_type[employment_type_id] (Many-to-One)

2. For skills (many-to-many):
   - fact_posting[posting_id] → bridge_posting_skill[posting_id] (One-to-Many)
   - bridge_posting_skill[skill_id] → dim_skill[skill_id] (Many-to-One)
   - Set bridge table cardinality to handle many-to-many

### Mark as Date Table
- If creating a separate date dimension, mark it as Date Table in Power BI
- Otherwise, use posted_date directly in fact_posting

---

## Future Enhancements

1. **Add Date Dimension (dim_date)**
   - Enables time intelligence: YoY growth, MTD, YTD, etc.
   - Attributes: Year, Quarter, Month, Week, Day, IsWeekend, IsHoliday

2. **Add Junk Dimension**
   - Combine low-cardinality flags (e.g., is_verified, is_featured, requires_relocation)

3. **Implement Type 2 SCD**
   - Track historical changes for company growth, industry shifts

4. **Add Aggregated Fact Tables**
   - Monthly snapshot fact table for faster trend queries

5. **Add Data Lineage Metadata**
   - Track when each record was loaded, source file, ETL run ID

---

## References

- Kimball, Ralph. *The Data Warehouse Toolkit* (3rd Edition)
- Star Schema Design Best Practices
- Power BI Data Modeling Documentation

---

**Last Updated:** 2024
**Author:** Analytics Portfolio Project
