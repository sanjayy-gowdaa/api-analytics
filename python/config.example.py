"""
Configuration file for API Analytics
Set your preferred data source: 'SQL' or 'CSV'

INSTRUCTIONS:
1. Copy this file and rename it to 'config.py'
2. Update the database credentials in config.py
3. Never commit config.py (it's in .gitignore for security)
"""

# Data source configuration: 'SQL' or 'CSV'
DATA_SOURCE = 'CSV'  # Change to 'SQL' to use MySQL database

# MySQL Database Configuration (only used if DATA_SOURCE = 'SQL')
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'apidb',
    'user': 'your_username',      # ⚠️ CHANGE THIS
    'password': 'your_password'   # ⚠️ CHANGE THIS
}

# CSV File Paths (only used if DATA_SOURCE = 'CSV')
CSV_CONFIG = {
    'input_file': '../querypart/api_logs_myql.csv',
    'api_metrics_output': 'api_metrics.csv',
    'funnel_metrics_output': 'funnel_metrics.csv',
    'region_metrics_output': 'region_metrics.csv'
}
