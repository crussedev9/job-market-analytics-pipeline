"""
Configuration for Glassdoor Data Science Jobs Dataset

This file maps the Glassdoor dataset columns to our dimensional model.

Expected Glassdoor CSV columns:
- Job Title
- Salary Estimate
- Job Description
- Rating
- Company Name
- Location
- Headquarters
- Size
- Founded
- Type of ownership
- Industry
- Sector
- Revenue
- Competitors (sometimes)
- Easy Apply (sometimes)
"""

# Column name mappings (Glassdoor → Our Schema)
COLUMN_MAPPING = {
    'Job Title': 'job_title',
    'Salary Estimate': 'salary_estimate',
    'Job Description': 'job_description',
    'Rating': 'company_rating',
    'Company Name': 'company_name',
    'Location': 'location',
    'Headquarters': 'headquarters',
    'Size': 'company_size',
    'Founded': 'company_founded',
    'Type of ownership': 'ownership_type',
    'Industry': 'industry',
    'Sector': 'sector',
    'Revenue': 'revenue',
    'Easy Apply': 'easy_apply'
}

# Skills dictionary for extraction from job descriptions
SKILLS_DICT = {
    'Programming Languages': [
        'Python', 'R', 'SQL', 'Java', 'Scala', 'C++', 'JavaScript', 'Julia',
        'MATLAB', 'SAS', 'Perl', 'Ruby', 'Go', 'Rust'
    ],
    'Databases': [
        'MySQL', 'PostgreSQL', 'MongoDB', 'Cassandra', 'Redis', 'Oracle',
        'SQL Server', 'SQLite', 'DynamoDB', 'BigQuery', 'Snowflake', 'Redshift'
    ],
    'BI Tools': [
        'Tableau', 'Power BI', 'Looker', 'QlikView', 'Qlik Sense', 'Sisense',
        'Domo', 'Metabase', 'Chartio', 'Mode Analytics'
    ],
    'Cloud Platforms': [
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'IBM Cloud', 'Oracle Cloud',
        'Databricks', 'Snowflake'
    ],
    'Data Engineering': [
        'Spark', 'Hadoop', 'Kafka', 'Airflow', 'Hive', 'Presto', 'Flink',
        'Beam', 'Luigi', 'Prefect', 'dbt', 'Fivetran', 'Talend', 'Informatica'
    ],
    'Machine Learning': [
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'XGBoost', 'LightGBM',
        'H2O', 'MLflow', 'Kubeflow', 'SageMaker', 'AutoML'
    ],
    'Analytics Tools': [
        'Excel', 'Google Sheets', 'Jupyter', 'RStudio', 'Stata', 'SPSS',
        'Alteryx', 'Knime', 'RapidMiner'
    ],
    'Data Visualization': [
        'D3.js', 'Plotly', 'Matplotlib', 'Seaborn', 'ggplot2', 'Bokeh',
        'Shiny', 'Dash', 'Streamlit'
    ],
    'Version Control': [
        'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN'
    ],
    'Statistics': [
        'Statistics', 'A/B Testing', 'Hypothesis Testing', 'Regression',
        'Time Series', 'Bayesian', 'Experimental Design'
    ]
}

# Job title groupings
JOB_TITLE_GROUPS = {
    'Data Analyst': [
        'data analyst', 'business analyst', 'analytics analyst',
        'marketing analyst', 'financial analyst', 'product analyst'
    ],
    'Data Scientist': [
        'data scientist', 'machine learning scientist', 'research scientist',
        'applied scientist', 'quantitative analyst'
    ],
    'Data Engineer': [
        'data engineer', 'etl developer', 'big data engineer',
        'platform engineer', 'pipeline engineer'
    ],
    'Analytics Engineer': [
        'analytics engineer', 'bi engineer', 'data analytics engineer'
    ],
    'BI Analyst': [
        'bi analyst', 'business intelligence analyst', 'bi developer',
        'tableau developer', 'power bi developer'
    ],
    'ML Engineer': [
        'machine learning engineer', 'ml engineer', 'mlops engineer',
        'ai engineer'
    ],
    'Data Manager': [
        'data manager', 'analytics manager', 'data science manager',
        'bi manager', 'director of', 'head of data', 'chief data officer'
    ]
}

# Seniority levels
SENIORITY_KEYWORDS = {
    'Junior': ['junior', 'jr', 'entry', 'associate', 'i ', 'intern'],
    'Mid-level': ['ii ', 'mid', 'intermediate'],
    'Senior': ['senior', 'sr', 'iii ', 'lead', 'principal', 'staff'],
    'Management': ['manager', 'director', 'head of', 'vp', 'vice president', 'chief', 'cto', 'cdo']
}

# Remote keywords
REMOTE_KEYWORDS = [
    'remote', 'work from home', 'wfh', 'telecommute', 'virtual',
    'anywhere', 'distributed'
]

# Employment type keywords
EMPLOYMENT_KEYWORDS = {
    'Full-time': ['full-time', 'full time', 'ft', 'permanent', 'regular'],
    'Contract': ['contract', 'contractor', 'temp', 'temporary', 'consultant'],
    'Part-time': ['part-time', 'part time', 'pt'],
    'Internship': ['intern', 'internship', 'co-op', 'coop']
}

# Company size standardization
COMPANY_SIZE_MAPPING = {
    '1 to 50 employees': '1-50',
    '51 to 200 employees': '51-200',
    '201 to 500 employees': '201-500',
    '501 to 1000 employees': '501-1000',
    '1001 to 5000 employees': '1001-5000',
    '5001 to 10000 employees': '5001-10000',
    '10000+ employees': '10000+',
    'Unknown': 'Unknown'
}
