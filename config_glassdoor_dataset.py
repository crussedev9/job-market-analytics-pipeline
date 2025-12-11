"""
Configuration for Glassdoor Data Science Jobs Dataset

This file maps the Glassdoor dataset columns to our dimensional model.

This version supports the nested column format from the comprehensive Glassdoor export:
- gaTrackerData.jobTitle (instead of "Job Title")
- gaTrackerData.location (instead of "Location")
- etc.
"""

# Column name mappings (Glassdoor nested format → Our Schema)
COLUMN_MAPPING = {
    # Job information
    'gaTrackerData.jobTitle': 'job_title',
    'header.jobTitle': 'job_title_header',  # Backup
    'job.description': 'job_description',

    # Salary information
    'header.payHigh': 'pay_high',
    'header.payLow': 'pay_low',
    'header.payPeriod': 'pay_period',
    'header.salaryHigh': 'salary_high',
    'header.salaryLow': 'salary_low',
    'header.salarySource': 'salary_source',

    # Company information
    'gaTrackerData.empName': 'company_name',
    'header.employerName': 'company_name_header',  # Backup
    'rating.starRating': 'company_rating',
    'overview.size': 'company_size',
    'overview.type': 'ownership_type',
    'overview.industry': 'industry',
    'overview.sector': 'sector',
    'overview.revenue': 'revenue',
    'overview.foundedYear': 'company_founded',

    # Location information
    'gaTrackerData.location': 'location',
    'header.location': 'location_header',  # Backup
    'overview.hq': 'headquarters',
    'map.country': 'country',
    'map.lat': 'latitude',
    'map.lng': 'longitude',

    # Application information
    'header.easyApply': 'easy_apply',
    'header.applyUrl': 'application_url',
    'header.posted': 'posted_date',

    # Additional metadata
    'header.employerId': 'employer_id',
    'gaTrackerData.jobId.long': 'job_id_external',
    'gaTrackerData.expired': 'is_expired',
}

# Skills dictionary for extraction from job descriptions
SKILLS_DICT = {
    'Programming Languages': [
        'Python', 'R', 'SQL', 'Java', 'Scala', 'C++', 'C#', 'JavaScript', 'Julia',
        'MATLAB', 'SAS', 'Perl', 'Ruby', 'Go', 'Rust', 'PHP', 'VBA'
    ],
    'Databases': [
        'MySQL', 'PostgreSQL', 'MongoDB', 'Cassandra', 'Redis', 'Oracle',
        'SQL Server', 'SQLite', 'DynamoDB', 'BigQuery', 'Snowflake', 'Redshift',
        'MariaDB', 'Neo4j', 'Elasticsearch', 'Teradata'
    ],
    'BI Tools': [
        'Tableau', 'Power BI', 'Looker', 'QlikView', 'Qlik Sense', 'Sisense',
        'Domo', 'Metabase', 'Chartio', 'Mode Analytics', 'SAP BusinessObjects',
        'MicroStrategy', 'Cognos', 'OBIEE'
    ],
    'Cloud Platforms': [
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'IBM Cloud', 'Oracle Cloud',
        'Databricks', 'Snowflake', 'Heroku', 'DigitalOcean'
    ],
    'Data Engineering': [
        'Spark', 'Hadoop', 'Kafka', 'Airflow', 'Hive', 'Presto', 'Flink',
        'Beam', 'Luigi', 'Prefect', 'dbt', 'Fivetran', 'Talend', 'Informatica',
        'NiFi', 'Stitch', 'Matillion'
    ],
    'Machine Learning': [
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'scikit-learn', 'XGBoost', 'LightGBM',
        'H2O', 'MLflow', 'Kubeflow', 'SageMaker', 'AutoML', 'Random Forest',
        'Neural Network', 'Deep Learning', 'Machine Learning', 'ML'
    ],
    'Analytics Tools': [
        'Excel', 'Google Sheets', 'Jupyter', 'RStudio', 'Stata', 'SPSS',
        'Alteryx', 'Knime', 'RapidMiner', 'Google Analytics', 'Mixpanel',
        'Amplitude', 'Segment'
    ],
    'Data Visualization': [
        'D3.js', 'Plotly', 'Matplotlib', 'Seaborn', 'ggplot2', 'Bokeh',
        'Shiny', 'Dash', 'Streamlit', 'Highcharts', 'Chart.js'
    ],
    'Version Control': [
        'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN'
    ],
    'Statistics': [
        'Statistics', 'Statistical', 'A/B Testing', 'Hypothesis Testing', 'Regression',
        'Time Series', 'Bayesian', 'Experimental Design', 'Predictive Modeling',
        'Forecasting'
    ],
    'Big Data': [
        'Big Data', 'Data Lake', 'Data Warehouse', 'ETL', 'ELT', 'Data Pipeline'
    ],
    'Other Skills': [
        'Docker', 'Kubernetes', 'Linux', 'Bash', 'API', 'REST', 'NoSQL',
        'Agile', 'Scrum', 'CI/CD', 'Jenkins'
    ]
}

# Job title groupings
JOB_TITLE_GROUPS = {
    'Data Analyst': [
        'data analyst', 'business analyst', 'analytics analyst',
        'marketing analyst', 'financial analyst', 'product analyst',
        'reporting analyst', 'insights analyst'
    ],
    'Data Scientist': [
        'data scientist', 'machine learning scientist', 'research scientist',
        'applied scientist', 'quantitative analyst', 'statistician'
    ],
    'Data Engineer': [
        'data engineer', 'etl developer', 'big data engineer',
        'platform engineer', 'pipeline engineer', 'data warehouse engineer'
    ],
    'Analytics Engineer': [
        'analytics engineer', 'bi engineer', 'data analytics engineer'
    ],
    'BI Analyst': [
        'bi analyst', 'business intelligence analyst', 'bi developer',
        'tableau developer', 'power bi developer', 'looker analyst'
    ],
    'ML Engineer': [
        'machine learning engineer', 'ml engineer', 'mlops engineer',
        'ai engineer', 'deep learning engineer'
    ],
    'Data Manager': [
        'data manager', 'analytics manager', 'data science manager',
        'bi manager', 'director of', 'head of data', 'chief data officer',
        'vp of data', 'vp data'
    ]
}

# Seniority levels
SENIORITY_KEYWORDS = {
    'Junior': ['junior', 'jr', 'jr.', 'entry', 'entry-level', 'associate', ' i ', 'intern', 'entry level'],
    'Mid-level': [' ii ', 'mid-level', 'mid level', 'intermediate'],
    'Senior': ['senior', 'sr', 'sr.', ' iii ', 'lead', 'principal', 'staff', 'expert'],
    'Management': ['manager', 'director', 'head of', 'vp', 'vice president', 'chief', 'cto', 'cdo', 'executive']
}

# Remote keywords
REMOTE_KEYWORDS = [
    'remote', 'work from home', 'wfh', 'telecommute', 'virtual',
    'anywhere', 'distributed', 'work-from-home', 'home-based',
    'remote position', 'remote opportunity', 'fully remote', '100% remote'
]

# Employment type keywords
EMPLOYMENT_KEYWORDS = {
    'Full-time': ['full-time', 'full time', 'ft', 'permanent', 'regular'],
    'Contract': ['contract', 'contractor', 'temp', 'temporary', 'consultant', 'freelance'],
    'Part-time': ['part-time', 'part time', 'pt'],
    'Internship': ['intern', 'internship', 'co-op', 'coop', 'summer intern']
}

# Company size standardization
COMPANY_SIZE_MAPPING = {
    '1 to 50 Employees': '1-50',
    '51 to 200 Employees': '51-200',
    '201 to 500 Employees': '201-500',
    '501 to 1000 Employees': '501-1000',
    '1001 to 5000 Employees': '1001-5000',
    '5001 to 10000 Employees': '5001-10000',
    '10000+ Employees': '10000+',
    '1 to 50 employees': '1-50',
    '51 to 200 employees': '51-200',
    '201 to 500 employees': '201-500',
    '501 to 1000 employees': '501-1000',
    '1001 to 5000 employees': '1001-5000',
    '5001 to 10000 employees': '5001-10000',
    '10000+ employees': '10000+',
    'Unknown / Non-Applicable': 'Unknown',
    'Unknown': 'Unknown',
    '': 'Unknown'
}
