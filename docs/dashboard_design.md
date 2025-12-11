# Dashboard Design Specification

## Executive Summary

The **Job Market Analytics Dashboard** is an interactive Power BI dashboard that provides insights into the data and analytics job market. It answers critical questions for job seekers, recruiters, and hiring managers about skills demand, compensation trends, work arrangements, and geographic opportunities.

**Target Audience:**
- Job seekers planning their career path
- Recruiters identifying talent pools
- HR professionals benchmarking compensation
- Educators designing curriculum

---

## Dashboard Purpose

### Primary Objectives

1. **Skills Intelligence:** Identify which technical skills are most in demand
2. **Compensation Benchmarking:** Understand salary ranges by role, location, and seniority
3. **Work Arrangement Trends:** Track remote vs on-site vs hybrid opportunities
4. **Geographic Insights:** Discover where analytics jobs are concentrated
5. **Career Planning:** Help job seekers make data-driven career decisions

### Key Business Questions

- Which skills should I learn to maximize job opportunities?
- What is the expected salary for my role and location?
- How prevalent are remote opportunities in analytics?
- Which companies are hiring most actively?
- How do salaries vary by seniority level?
- What skills correlate with higher compensation?

---

## Dashboard Pages

### Page 1: Executive Overview

**Purpose:** High-level summary of job market trends

**Layout:**
```
┌────────────────────────────────────────────────────────────────┐
│  Title: Job Market Analytics - Executive Overview              │
│  Subtitle: Data & Analytics Roles - Last Updated: [Date]       │
├─────────┬─────────┬─────────┬─────────┬─────────┬─────────────┤
│  Total  │   Avg   │ Median  │   %     │  Top    │     Top     │
│ Postings│ Salary  │ Salary  │ Remote  │  Skill  │  Location   │
│ [12,543]│ [$95K]  │ [$88K]  │ [42%]   │ [SQL]   │ [SF Bay]    │
├─────────┴─────────┴─────────┴─────────┴─────────┴─────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │  Line Chart: Posting Volume Trend (Last 12 Months) │       │
│  │                                                     │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
├──────────────────────────────────┬──────────────────────────────┤
│  Bar: Top 10 Locations           │  Donut: Work Arrangement     │
│  1. San Francisco Bay Area       │    Remote: 42%               │
│  2. New York Metro                │    Hybrid: 33%               │
│  3. Seattle                       │    On-site: 25%              │
│  ...                             │                              │
└──────────────────────────────────┴──────────────────────────────┘
```

**Visuals:**

1. **KPI Cards (Top Row)**
   - Total Postings: COUNT(posting_id)
   - Avg Salary: AVG(salary_midpoint)
   - Median Salary: MEDIAN(salary_midpoint)
   - % Remote: Calculated measure
   - Top Skill: Most frequent skill
   - Top Location: Location with most postings

2. **Line Chart: Posting Volume Trend**
   - X-axis: Month
   - Y-axis: Count of postings
   - Trend line: 3-month moving average
   - Data label on latest month

3. **Horizontal Bar Chart: Top Locations**
   - Top 10 cities/metro areas
   - Sorted by posting count (descending)
   - Data labels showing count
   - Conditional formatting: gradient based on count

4. **Donut Chart: Work Arrangement**
   - Segments: Remote, Hybrid, On-site
   - Data labels: percentage
   - Legend positioned on right

**Interactivity:**
- Global date range slicer (top right)
- Job category slicer (sidebar)
- Click on location to filter other visuals
- Drill-through to Page 6 (Posting Details)

---

### Page 2: Skills Deep Dive

**Purpose:** Analyze technical skills in demand

**Layout:**
```
┌────────────────────────────────────────────────────────────────┐
│  Title: Skills in Demand                                       │
├────────────────────────────────┬───────────────────────────────┤
│                                │  Tree Map: Skills by Category │
│  Horizontal Bar: Top 20 Skills │  [Programming] [BI Tools]     │
│  1. SQL            [5,234]     │  [Cloud] [Databases]          │
│  2. Python         [4,891]     │                               │
│  3. Excel          [4,502]     │                               │
│  4. Power BI       [3,876]     │                               │
│  5. Tableau        [3,234]     │                               │
│  ...                           │                               │
│                                │                               │
├────────────────────────────────┴───────────────────────────────┤
│  Scatter Plot: Avg Salary vs Posting Count by Skill            │
│  (Bubble size = skill frequency)                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Visuals:**

1. **Horizontal Bar Chart: Top 20 Skills**
   - Y-axis: Skill name
   - X-axis: Posting count
   - Sorted descending by count
   - Conditional formatting: top 5 skills highlighted
   - Data labels on bars
   - Interactive: Click to filter dashboard

2. **Tree Map: Skills by Category**
   - Groups: Programming, BI Tools, Cloud, Databases, Analytics
   - Size: Posting count
   - Color: Average salary (gradient)
   - Tooltip: Skill name, count, avg salary

3. **Scatter Plot: Salary vs Demand**
   - X-axis: Posting count
   - Y-axis: Average salary for jobs requiring this skill
   - Bubble size: Skill frequency
   - Quadrant lines: Median posting count, median salary
   - Insight: Top-right quadrant = high demand + high salary

4. **Matrix Table: Skill Co-Occurrence (Optional)**
   - Rows: Skills
   - Columns: Skills
   - Values: Count of postings requiring both skills
   - Conditional formatting: heat map

**Filters:**
- Job category (Data Analytics, Data Science, etc.)
- Seniority level
- Work arrangement
- Minimum posting count (e.g., show only skills with 50+ postings)

**Calculated Measures:**
```DAX
Skill Posting Count =
    CALCULATE(COUNTROWS(bridge_posting_skill))

Avg Salary for Skill =
    CALCULATE(
        AVERAGE(fact_posting[salary_midpoint]),
        bridge_posting_skill
    )

Skill Demand Rank =
    RANKX(
        ALL(dim_skill[skill_name]),
        [Skill Posting Count],
        ,
        DESC
    )
```

---

### Page 3: Compensation Analysis

**Purpose:** Benchmark salaries across dimensions

**Layout:**
```
┌────────────────────────────────────────────────────────────────┐
│  Title: Compensation Insights                                  │
├────────────────────────────────┬───────────────────────────────┤
│  Histogram: Salary Distribution│  Box Plot: Salary by Seniority│
│  (Salary Midpoint)             │  Junior ──○──                 │
│  ████                          │  Mid     ────○────            │
│   ████████                     │  Senior      ─────○─────      │
│       ████████                 │  Lead            ────○────    │
│           ████                 │  Exec              ──○──      │
├────────────────────────────────┴───────────────────────────────┤
│  Map Visual: Avg Salary by Location                            │
│  (Bubble size = posting count, color = avg salary)             │
│                                                                 │
├────────────────────────────────────────────────────────────────┤
│  Table: Salary Statistics by Job Title                         │
│  Job Title        | Avg   | Min   | Max    | Median | Count   │
│  ───────────────────────────────────────────────────────────   │
│  Senior Data Eng  | $125K | $90K  | $180K  | $120K  | 342     │
│  Data Scientist   | $118K | $75K  | $175K  | $115K  | 521     │
│  ...                                                            │
└────────────────────────────────────────────────────────────────┘
```

**Visuals:**

1. **Histogram: Salary Distribution**
   - X-axis: Salary bins ($10K increments)
   - Y-axis: Count of postings
   - Normal distribution overlay (optional)
   - Mean and median lines

2. **Box and Whisker Plot: Salary by Seniority**
   - Categories: Junior, Mid, Senior, Lead, Executive
   - Shows min, Q1, median, Q3, max
   - Outliers displayed as points
   - Sort by median salary (ascending)

3. **Map Visual: Geographic Salary**
   - Filled map (choropleth) by state, OR
   - Bubble map by city (size = count, color = avg salary)
   - Tooltip: Location, avg salary, posting count, % remote

4. **Table: Salary Stats by Job Title**
   - Columns: Job Title, Avg Salary, Min, Max, Median, Posting Count
   - Sort by any column
   - Conditional formatting: Color scale on avg salary
   - Filter: Show only titles with 10+ postings

**Slicers:**
- Seniority level
- Location (state/city)
- Job category
- Work arrangement (remote/hybrid/on-site)

**Calculated Columns:**
```DAX
Salary Band =
    SWITCH(
        TRUE(),
        [salary_midpoint] < 50000, "< $50K",
        [salary_midpoint] < 75000, "$50K - $75K",
        [salary_midpoint] < 100000, "$75K - $100K",
        [salary_midpoint] < 130000, "$100K - $130K",
        [salary_midpoint] < 160000, "$130K - $160K",
        "$160K+"
    )
```

**Insights Section:**
- Text box: "Median salary increases by $25K from Mid to Senior level"
- Text box: "Remote positions pay 7% more on average than on-site"

---

### Page 4: Geographic Insights

**Purpose:** Understand location-based opportunities

**Layout:**
```
┌────────────────────────────────────────────────────────────────┐
│  Title: Where Are the Jobs?                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Filled Map: Posting Density by State                          │
│  (Darker color = more postings)                                │
│                                                                 │
├──────────────────────────────────┬─────────────────────────────┤
│  Table: City-Level Metrics       │  Bar: Top 15 Metro Areas    │
│  City | State | Count | Avg Sal  │  1. SF Bay Area   [2,341]  │
│  SF   | CA    | 2341  | $115K    │  2. NYC Metro     [1,987]  │
│  NYC  | NY    | 1987  | $108K    │  3. Seattle       [1,234]  │
│  ...                             │  ...                        │
└──────────────────────────────────┴─────────────────────────────┘
```

**Visuals:**

1. **Filled Map (Choropleth): Posting Density**
   - Geography: US States
   - Color saturation: Posting count
   - Tooltip: State, count, avg salary, % remote

2. **Bubble Map (Alternative): Jobs by City**
   - Bubble size: Posting count
   - Bubble color: Average salary (gradient)
   - Tooltip: City, state, count, avg salary, top skill

3. **Table: City-Level Detail**
   - Columns: City, State, Posting Count, Avg Salary, % Remote
   - Sort by posting count (descending)
   - Search box: Find specific city
   - Export to Excel enabled

4. **Horizontal Bar Chart: Top Metro Areas**
   - Top 15 metro areas
   - Data labels with count
   - Click to filter map and table

**Filters:**
- Remote jobs included/excluded toggle
- Minimum posting count slider
- Job category
- Salary range

**Insights:**
- Call-out: "Top 5 cities represent 45% of all analytics jobs"
- KPI card: "32 states with 100+ analytics job postings"

---

### Page 5: Work Arrangement Trends

**Purpose:** Analyze remote/hybrid/on-site patterns

**Layout:**
```
┌────────────────────────────────────────────────────────────────┐
│  Title: Remote Work Trends                                     │
├────────────────────────────────────────────────────────────────┤
│  Stacked Area Chart: Work Arrangement Over Time                │
│  (If date available)                                           │
│  ░░░░ Remote  ▓▓▓▓ Hybrid  ████ On-site                       │
│                                                                 │
├──────────────────────────────────┬─────────────────────────────┤
│  100% Stacked Bar: By Job Cat   │  Donut: Overall Distribution│
│  Data Analytics   ███▓▓░░        │  Remote: 42%                │
│  Data Science     ████▓░         │  Hybrid: 33%                │
│  Data Engineering ███▓▓░         │  On-site: 25%               │
│  BI Analyst       ██▓▓░░░        │                             │
├──────────────────────────────────┴─────────────────────────────┤
│  Table: Work Arrangement by Company Size                       │
│  Company Size | Remote % | Hybrid % | On-site % | Total        │
│  1-50         | 55%      | 25%      | 20%       | 1,234        │
│  51-200       | 48%      | 32%      | 20%       | 2,456        │
│  ...                                                            │
└────────────────────────────────────────────────────────────────┘
```

**Visuals:**

1. **Stacked Area Chart: Trends Over Time**
   - X-axis: Month/Quarter
   - Y-axis: Count or percentage
   - Series: Remote, Hybrid, On-site
   - Trend: Is remote increasing?

2. **100% Stacked Bar Chart: By Job Category**
   - Categories: Data Analytics, Data Science, BI, etc.
   - Segments: Remote, Hybrid, On-site
   - Data labels: percentages
   - Insight: Which roles are most remote-friendly?

3. **Donut Chart: Overall Distribution**
   - Segments: Remote, Hybrid, On-site
   - Percentages displayed
   - Color-coded (green = remote, blue = hybrid, gray = on-site)

4. **Table: By Company Size**
   - Rows: Company size buckets
   - Columns: % Remote, % Hybrid, % On-site, Total postings
   - Insight: Larger companies more likely to offer hybrid?

**Filters:**
- Date range
- Job category
- Seniority level

**Calculated Measures:**
```DAX
% Remote Positions =
    DIVIDE(
        CALCULATE(COUNTROWS(fact_posting), dim_employment_type[work_arrangement] = "Remote"),
        COUNTROWS(fact_posting)
    )

Remote Trend (YoY) =
    VAR CurrentPct = [% Remote Positions]
    VAR PriorYearPct = CALCULATE([% Remote Positions], DATEADD(fact_posting[posted_date], -1, YEAR))
    RETURN CurrentPct - PriorYearPct
```

---

### Page 6: Posting Details (Drill-Through)

**Purpose:** Searchable detail table for drill-through

**Layout:**
```
┌────────────────────────────────────────────────────────────────┐
│  Title: Job Posting Details                                    │
│  [Search Box: Filter by keyword]                               │
├────────────────────────────────────────────────────────────────┤
│  Table: All Job Postings                                       │
│  ID  | Job Title        | Company | Location | Salary  | Skills│
│  123 | Sr Data Analyst  | Acme    | SF, CA   | $90-120K| SQL...│
│  124 | Data Scientist   | TechCo  | Remote   | $100-140│ Python│
│  ...                                                            │
│  [Export to Excel]                                             │
└────────────────────────────────────────────────────────────────┘
```

**Visuals:**

1. **Table Visual: Complete Posting Details**
   - Columns (customizable):
     - Posting ID
     - Job Title
     - Company
     - Location
     - Salary Range
     - Work Arrangement
     - Seniority Level
     - Skill Count
     - Application URL (clickable link)
   - Pagination: 25 rows per page
   - Sort by any column
   - Search/filter on all fields

**Drill-Through Setup:**
- Set as drill-through target from all other pages
- Drill-through filters: Automatically applied from source visual
- Back button: Return to source page

**Interactivity:**
- Click URL to open application page (external link)
- Right-click on company name → "See all jobs from this company"

---

## Global Design Elements

### Color Palette

**Primary Colors:**
- Blue: `#0078D4` (professional, analytics theme)
- Teal: `#00B294` (secondary, growth)
- Orange: `#FF8C00` (accent, alerts)

**Semantic Colors:**
- Green: `#107C10` (positive, remote)
- Red: `#D13438` (negative, below benchmark)
- Gray: `#605E5C` (neutral, on-site)

**Gradients:**
- Low to High: Light Blue → Dark Blue
- Salary: Yellow → Orange → Red

### Typography

- **Page Titles:** Segoe UI Bold, 18pt, #000000
- **Section Headers:** Segoe UI Semibold, 14pt, #323130
- **Body Text:** Segoe UI Regular, 10pt, #605E5C
- **KPI Values:** Segoe UI Light, 32pt, #0078D4
- **Data Labels:** Segoe UI Regular, 9pt, #323130

### Layout Principles

1. **Consistent Spacing:** 16px grid
2. **Visual Hierarchy:** Most important metrics at top
3. **F-Pattern Reading:** Key info in top-left
4. **White Space:** Avoid clutter, use breathing room
5. **Alignment:** Grid-based, aligned edges

### Accessibility

- **High Contrast Mode:** Support Windows high contrast themes
- **Alt Text:** All visuals have descriptive alt text
- **Keyboard Navigation:** Tab order configured logically
- **Screen Readers:** ARIA labels on custom visuals
- **Color Blind Friendly:** Don't rely solely on color (use shapes, labels)

---

## Interactivity & Navigation

### Global Filters (Apply to All Pages)

Located in left sidebar (collapsible):
- **Date Range:** Last 12 months default, custom range option
- **Job Category:** Multi-select (Analytics, Data Science, BI, Engineering)
- **Seniority Level:** Multi-select (Junior, Mid, Senior, Lead, Executive)
- **Work Arrangement:** Multi-select (Remote, Hybrid, On-site)
- **Minimum Salary:** Slider (default: $0)

### Page Navigation

- **Navigation Bar:** Top of dashboard
- **Tabs:** Overview | Skills | Compensation | Geography | Work Trends | Details
- **Breadcrumbs:** Show current page and filter context
- **Home Button:** Return to Overview page

### Bookmarks

Pre-configured views for quick access:
1. **"Remote Only"** → Filters to work_arrangement = Remote
2. **"Senior Roles"** → Filters to seniority_level = Senior, Lead, Principal
3. **"High Salary"** → Filters to salary_min >= $100K
4. **"Analytics Engineers"** → Filters to job_title contains "Analytics Engineer"
5. **"Top Skills Only"** → Filters to top 10 skills by demand

### Drill-Through Actions

- From any visual → Page 6 (Posting Details)
- Filters automatically applied based on selection
- Example: Click "Python" skill → See all Python jobs

### Cross-Filtering

- **Enabled by default** across visuals on same page
- Click on a bar/segment → Other visuals filter to that selection
- Click again to clear filter
- Ctrl+Click to multi-select

### Tooltips

**Custom Tooltips** (report page tooltips):
- Hover over skill → Show skill description, related skills, avg salary
- Hover over company → Show company size, industry, posting count
- Hover over location → Show cost of living index (if data available)

---

## Calculated Measures (DAX)

### Core Measures

```DAX
// Basic aggregations
Total Postings = COUNTROWS(fact_posting)
Avg Salary = AVERAGE(fact_posting[salary_midpoint])
Median Salary = MEDIAN(fact_posting[salary_midpoint])
Min Salary = MIN(fact_posting[salary_min])
Max Salary = MAX(fact_posting[salary_max])

// Percentages
% Remote =
    DIVIDE(
        CALCULATE([Total Postings], dim_employment_type[work_arrangement] = "Remote"),
        [Total Postings],
        0
    )

% with Salary Data =
    DIVIDE(
        CALCULATE([Total Postings], NOT(ISBLANK(fact_posting[salary_midpoint]))),
        [Total Postings],
        0
    )

// Rankings
Location Rank =
    RANKX(
        ALL(dim_location[city]),
        [Total Postings],
        ,
        DESC,
        DENSE
    )

Skill Demand Rank =
    RANKX(
        ALL(dim_skill[skill_name]),
        [Skill Posting Count],
        ,
        DESC
    )

// Time intelligence (requires date table)
Postings YTD = TOTALYTD([Total Postings], dim_date[Date])

Postings vs Last Year =
    [Total Postings] - CALCULATE([Total Postings], SAMEPERIODLASTYEAR(dim_date[Date]))

YoY Growth % =
    DIVIDE([Postings vs Last Year], CALCULATE([Total Postings], SAMEPERIODLASTYEAR(dim_date[Date])), 0)

// Advanced
Salary 25th Percentile = PERCENTILE.INC(fact_posting[salary_midpoint], 0.25)
Salary 75th Percentile = PERCENTILE.INC(fact_posting[salary_midpoint], 0.75)

Avg Skills per Posting =
    AVERAGEX(
        fact_posting,
        CALCULATE(COUNTROWS(bridge_posting_skill))
    )
```

---

## Data Refresh

### Refresh Schedule (If Published to Power BI Service)

- **Frequency:** Weekly (every Monday at 6 AM)
- **Method:** Incremental refresh (future enhancement)
- **Notifications:** Email on refresh failure

### Manual Refresh (Desktop)

- **Refresh Button:** Updates all queries and visuals
- **Duration:** < 5 minutes for 50K postings

---

## Performance Optimization

### Data Model Optimizations

1. **Minimize Row Count:** Filter data in Power Query (e.g., last 12 months only)
2. **Remove Unused Columns:** Only load necessary columns
3. **Use Star Schema:** Optimized for aggregation queries
4. **Avoid Calculated Columns:** Use measures instead (computed on demand)

### Visual Optimizations

1. **Limit Visuals per Page:** Max 8-10 visuals
2. **Avoid Custom Visuals:** Use native visuals when possible
3. **Reduce Unique Values:** Limit categories in charts (e.g., top 20)
4. **Use Aggregated Views:** Pre-aggregate in SQL views

---

## Testing & Validation

### Functionality Testing

- [ ] All slicers filter visuals correctly
- [ ] Cross-filtering works as expected
- [ ] Drill-through navigates to detail page
- [ ] Bookmarks apply filters correctly
- [ ] Export to Excel works
- [ ] External links (application URLs) open correctly

### Data Validation

- [ ] KPI totals match SQL query results
- [ ] Salary calculations (avg, median) are accurate
- [ ] Skill counts match bridge table
- [ ] No orphaned records displayed

### UX Testing

- [ ] Dashboard loads in < 10 seconds
- [ ] Navigation is intuitive
- [ ] Visuals are readable at 1920x1080 resolution
- [ ] Mobile layout is functional
- [ ] Accessible via keyboard navigation

---

## Deployment

### Option 1: Desktop Sharing

- Save `.pbix` file to shared drive or email
- Users open in Power BI Desktop (free download)
- Manual refresh required

### Option 2: Power BI Service (Cloud)

- Publish to Power BI workspace
- Share via web link or embed in SharePoint
- Schedule automated refresh
- Requires Power BI Pro license

### Option 3: Static Export

- Export pages to PDF for presentations
- Share screenshots for email reports
- No interactivity, but universally accessible

---

## Maintenance & Updates

### Regular Updates

- **Data Refresh:** Weekly (when new job postings available)
- **Visual Tweaks:** Quarterly (based on user feedback)
- **New Pages:** As new business questions emerge

### Version Control

- Save dashboard versions with date suffix: `Dashboard_v1.0_2024-03-15.pbix`
- Maintain changelog in README

---

**Last Updated:** 2024
**Author:** Analytics Portfolio Project
