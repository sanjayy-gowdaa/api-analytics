"""
SQL Connector for MySQL Database
Executes SQL queries and returns DataFrames matching the Pandas output format
"""

import pandas as pd
import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Establish connection to MySQL database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        raise


def get_api_metrics():
    """
    Fetch API performance metrics from MySQL
    Returns DataFrame with columns: api_name, total_requests, success_rate, 
                                    avg_latency_ms, p95_latency_ms, top_error_reason
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total requests and success rate
    query_base = """
    SELECT 
        api_name,
        COUNT(*) as total_requests,
        ROUND(SUM(CASE WHEN status_Code=200 THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) as success_rate,
        ROUND(AVG(latency_ms), 2) as avg_latency_ms
    FROM api_logs
    GROUP BY api_name
    """
    
    df_base = pd.read_sql(query_base, conn)
    
    # P95 latency calculation
    query_p95 = """
    SELECT api_name,
           ANY_VALUE(latency_ms) as p95_latency_ms
    FROM (
        SELECT api_name,
               latency_ms,
               NTILE(20) OVER(PARTITION BY api_name ORDER BY latency_ms) as tile
        FROM api_logs
    ) t 
    WHERE tile = 19
    GROUP BY api_name
    """
    
    df_p95 = pd.read_sql(query_p95, conn)
    
    # Top error reason per API
    query_errors = """
    SELECT api_name,
           error_reason as top_error_reason
    FROM (
        SELECT api_name,
               error_reason,
               COUNT(*) as error_count,
               ROW_NUMBER() OVER(PARTITION BY api_name ORDER BY COUNT(*) DESC) as rn
        FROM api_logs
        WHERE status_Code != 200
        GROUP BY api_name, error_reason
    ) ranked_errors
    WHERE rn = 1
    """
    
    df_errors = pd.read_sql(query_errors, conn)
    
    # Merge all metrics
    df_metrics = df_base.merge(df_p95, on='api_name', how='left')
    df_metrics = df_metrics.merge(df_errors, on='api_name', how='left')
    
    # Fill NaN for APIs with no errors
    df_metrics['top_error_reason'] = df_metrics['top_error_reason'].fillna('')
    
    cursor.close()
    conn.close()
    
    return df_metrics


def get_funnel_metrics():
    """
    Fetch conversion funnel metrics from MySQL
    Returns DataFrame with columns: api_name, total_requests, successful_requests, conversion_rate
    """
    conn = get_connection()
    
    query = """
    SELECT 
        api_name,
        COUNT(*) as total_requests,
        SUM(CASE WHEN status_Code=200 THEN 1 ELSE 0 END) as successful_requests,
        ROUND(SUM(CASE WHEN status_Code=200 THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) as conversion_rate
    FROM api_logs
    GROUP BY api_name
    ORDER BY conversion_rate DESC
    """
    
    df_funnel = pd.read_sql(query, conn)
    conn.close()
    
    return df_funnel


def get_region_metrics():
    """
    Fetch region-wise performance metrics from MySQL
    Returns DataFrame with columns: region, total_requests, success_rate
    """
    conn = get_connection()
    
    query = """
    SELECT 
        region,
        COUNT(*) as total_requests,
        ROUND(SUM(CASE WHEN status_Code=200 THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) as success_rate
    FROM api_logs
    GROUP BY region
    ORDER BY success_rate DESC
    """
    
    df_region = pd.read_sql(query, conn)
    conn.close()
    
    return df_region


def test_connection():
    """Test database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM api_logs")
        count = cursor.fetchone()[0]
        print(f"✓ Successfully connected to database")
        print(f"✓ Found {count} records in api_logs table")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test the connection
    print("Testing MySQL connection...")
    test_connection()
