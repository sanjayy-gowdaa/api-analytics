"""
Configuration file for API Analytics
Set your preferred data source: 'SQL' or 'CSV'
"""

# Data source configuration: 'SQL' or 'CSV'
DATA_SOURCE = 'CSV'  # Change to 'SQL' to use MySQL database

# MySQL Database Configuration (only used if DATA_SOURCE = 'SQL')
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'apidb',
    'user': 'root',          # Change to your MySQL username
    'password': 'password'   # Change to your MySQL password
}

# CSV File Paths (only used if DATA_SOURCE = 'CSV')
CSV_CONFIG = {
    'input_file': '../querypart/api_logs_myql.csv',
    'api_metrics_output': 'api_metrics.csv',
    'funnel_metrics_output': 'funnel_metrics.csv',
    'region_metrics_output': 'region_metrics.csv'
}
