# Power BI Dashboard Layer

This folder is designated for the Power BI dashboard file(s) that visualize the job market analytics data.

## Dashboard Overview

**Dashboard Name:** Job Market Analytics Dashboard

**Purpose:** Provide interactive insights into the data and analytics job market, including skills demand, salary trends, remote work patterns, and geographic distribution of opportunities.

**Target Audience:**
- Job seekers in data/analytics fields
- Recruiters and talent acquisition teams
- HR professionals and hiring managers
- Career counselors and educators

---

## Data Connection

The Power BI dashboard connects to the data pipeline outputs through one of two methods:

### Option A: SQLite Database Connection (Recommended)
- **Source:** `job_market.db` (SQLite database in project root)
- **Views to Import:**
  - `vw_job_posting_details` - Denormalized posting details
  - `vw_salary_by_title_and_location` - Salary analysis
  - `vw_skill_demand` - Skills demand ranking
  - `vw_remote_vs_onsite_trends` - Work arrangement trends

### Option B: CSV File Connection
- **Source:** `data/processed/*.csv` files
- **Tables to Import:**
  - `fact_posting.csv`
  - `dim_job.csv`
  - `dim_company.csv`
  - `dim_location.csv`
  - `dim_employment_type.csv`
  - `dim_skill.csv`
  - `bridge_posting_skill.csv`
- **Note:** Relationships must be created manually in Power BI Model view

**Power Query Setup:**
- See `power_query/job_postings_power_query_m_code.txt` for M code templates
- Update file paths in the M code to match your local environment

---

## Planned Dashboard Pages

### Page 1: Executive Overview
**Purpose:** High-level KPIs and summary metrics

**Visuals:**
- **KPI Cards** (across the top):
  - Total Job Postings
  - Average Salary
  - Median Salary
  - % Remote Positions
  - Most In-Demand Skill
  - Top Hiring Location

- **Line Chart:** Job posting volume over time (by month)
- **Horizontal Bar Chart:** Top 10 locations by posting count
- **Donut Chart:** Remote vs Hybrid vs On-site breakdown
- **Table:** Recent postings (showing latest 10)

**Interactivity:**
- Date range slicer
- Job category slicer
- Drill-through to other pages

---

### Page 2: Skills Deep Dive
**Purpose:** Analyze which skills are most in demand

**Visuals:**
- **Horizontal Bar Chart:** Top 20 skills by posting count (sortable)
- **Tree Map:** Skills grouped by category (Programming, BI Tools, Cloud, etc.)
- **Scatter Plot:** Average salary vs posting count by skill
- **Matrix Table:** Skill co-occurrence (which skills appear together frequently)
- **Card:** Total unique skills

**Filters:**
- Job category (Data Analytics, Data Science, BI, etc.)
- Seniority level
- Work arrangement (Remote/Hybrid/On-site)

**Insights to Answer:**
- Which skills should I learn to maximize opportunities?
- Which skills correlate with higher salaries?
- What skill combinations are most common?

---

### Page 3: Compensation Analysis
**Purpose:** Explore salary trends and benchmarks

**Visuals:**
- **Histogram:** Salary distribution (midpoint)
- **Box and Whisker Plot:** Salary range by seniority level
- **Map Visual:** Average salary by location (bubble size = posting count)
- **Table:** Salary statistics by job title (avg, min, max, median)
- **Column Chart:** Average salary by job category

**Slicers:**
- Seniority level
- Location (state or city)
- Job category
- Remote vs on-site

**Calculated Measures (DAX):**
```DAX
Avg Salary Midpoint = AVERAGE(fact_posting[salary_midpoint])
Median Salary = MEDIAN(fact_posting[salary_midpoint])
Salary 25th Percentile = PERCENTILE.INC(fact_posting[salary_midpoint], 0.25)
Salary 75th Percentile = PERCENTILE.INC(fact_posting[salary_midpoint], 0.75)
```

---

### Page 4: Geographic Insights
**Purpose:** Understand where analytics jobs are concentrated

**Visuals:**
- **Filled Map:** Posting density by state (choropleth)
- **Bubble Map:** Posting count by city (size = count, color = avg salary)
- **Table:** City-level metrics (City, State, Posting Count, Avg Salary, % Remote)
- **Bar Chart:** Top 15 metro areas by posting volume
- **Small Multiples:** Posting count by state, faceted by job category

**Filters:**
- Remote jobs included/excluded
- Minimum posting count (to filter out low-volume locations)
- Salary range

---

### Page 5: Work Arrangement Trends
**Purpose:** Analyze remote, hybrid, and on-site work patterns

**Visuals:**
- **Stacked Area Chart:** Work arrangement breakdown over time
- **100% Stacked Bar Chart:** Work arrangement by job category
- **Donut Chart:** Overall work arrangement distribution
- **Table:** Work arrangement by company size
- **Line Chart:** % Remote positions trend over time

**Insights to Answer:**
- Is remote work increasing or decreasing?
- Which roles are most likely to be remote?
- How does work arrangement correlate with salary?

---

### Page 6: Posting Details (Drill-Through)
**Purpose:** Searchable, filterable table of all job postings

**Visuals:**
- **Table Visual:** All columns from `vw_job_posting_details`
  - Posting ID, Job Title, Company, Location, Salary Range, Skills Count, etc.
- **Search Box:** Free-text search across job titles and companies
- **Export Button:** Allow users to export filtered results to Excel

**Filters:**
- All dimension attributes (job title, company, location, etc.)

**Drill-Through From:**
- Any visual on other pages (e.g., click a skill to see all postings requiring that skill)

---

## Interactivity Features

### Global Slicers
Apply these across all pages (use bookmark groups):
- Date Range (posted_date)
- Job Category (Data Analytics, Data Science, BI, Engineering)
- Seniority Level (Junior, Mid, Senior, Lead, Executive)
- Work Arrangement (Remote, Hybrid, On-site)
- Minimum Salary

### Cross-Filtering
- Enable cross-filtering between visuals
- Click a bar in "Top Skills" to filter all other visuals by that skill

### Bookmarks
Create bookmarks for common views:
- "Remote Only" - filters to only remote positions
- "Senior Roles" - filters to Senior+ seniority
- "High Salary" - filters to salaries above $100K
- "Analytics Engineers" - filters to Analytics Engineer role

### Tooltips
Add rich tooltips showing:
- Salary range details when hovering over locations
- Skill descriptions when hovering over skill names
- Company info when hovering over company names

---

## Design Principles

### Color Scheme
- **Primary:** Blue tones (#0078D4, #005A9E) - professional, analytics-focused
- **Secondary:** Teal/green (#00B294, #008272) - growth, opportunity
- **Accent:** Orange (#FF8C00) - highlights, alerts
- **Neutral:** Grays for backgrounds and borders

### Typography
- **Headers:** Segoe UI Bold, 16-18pt
- **Body Text:** Segoe UI, 10-12pt
- **KPIs:** Segoe UI Light, 28-36pt

### Layout
- Consistent spacing (16px grid)
- Mobile-friendly design (test responsive layout)
- Accessibility: High contrast mode support, screen reader compatibility

---

## Dashboard File

**Filename:** `Job_Market_Analytics_Dashboard.pbix`

**Status:** To be added in a future update

**Data Refresh:**
- For demo purposes, data is static (loaded from SQLite or CSV)
- In production, could be scheduled for daily/weekly refresh

---

## Deployment Options

### Option 1: Desktop Only
- Share `.pbix` file directly
- Users open in Power BI Desktop (free)

### Option 2: Power BI Service (Cloud)
- Publish to Power BI Service (requires Pro license)
- Share via web link or embed in website
- Enable scheduled refresh

### Option 3: Export to PDF
- Export static reports as PDF for email distribution
- Good for executive summaries

---

## Calculated Measures (DAX Examples)

Add these measures to the Power BI data model:

```DAX
// Basic aggregations
Total Postings = COUNTROWS(fact_posting)
Avg Salary = AVERAGE(fact_posting[salary_midpoint])
Median Salary = MEDIAN(fact_posting[salary_midpoint])

// Percentage calculations
% Remote =
DIVIDE(
    CALCULATE(COUNTROWS(fact_posting), dim_employment_type[work_arrangement] = "Remote"),
    COUNTROWS(fact_posting),
    0
)

// Year-over-year growth
Posting Count YoY Growth % =
VAR CurrentYear = YEAR(TODAY())
VAR LastYear = CurrentYear - 1
VAR CurrentCount = CALCULATE(COUNTROWS(fact_posting), YEAR(fact_posting[posted_date]) = CurrentYear)
VAR LastCount = CALCULATE(COUNTROWS(fact_posting), YEAR(fact_posting[posted_date]) = LastYear)
RETURN
DIVIDE(CurrentCount - LastCount, LastCount, 0)

// Skill demand rank
Skill Rank =
RANKX(
    ALL(dim_skill[skill_name]),
    CALCULATE(COUNTROWS(bridge_posting_skill)),
    ,
    DESC,
    DENSE
)
```

---

## Future Enhancements

- Add drill-through to external job boards (clickable URLs)
- Implement AI-powered insights (Key Influencers visual)
- Add time intelligence for trend analysis
- Create mobile-optimized layout
- Add Q&A natural language querying
- Implement row-level security (if sharing widely)

---

## Usage Instructions

1. Ensure the ETL pipeline has been run and data is in `job_market.db` or `data/processed/`
2. Open Power BI Desktop
3. Use Power Query M code from `power_query/` folder to connect to data
4. Create relationships in Model view (if using CSV option)
5. Build dashboard pages following the specifications above
6. Save as `Job_Market_Analytics_Dashboard.pbix` in this folder

---

For detailed technical documentation, see:
- [Data Model Documentation](../docs/data_model.md)
- [Dashboard Design Specifications](../docs/dashboard_design.md)
