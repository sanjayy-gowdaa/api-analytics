"""
Aggregate Metrics Calculator
Supports both CSV (Pandas) and SQL (MySQL) data sources
Configure your preferred data source in config.py
"""

import pandas as pd
import numpy as np
from config import DATA_SOURCE, CSV_CONFIG


def calculate_metrics_from_csv():
    """Calculate metrics using Pandas from CSV file"""
    print("📊 Using CSV/Pandas approach...")
    
    df = pd.read_csv(CSV_CONFIG['input_file'])
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
    df["is_success"] = df["status_Code"] == 200

    def p95(series):
        return np.percentile(series, 95)
    
    def most_common_error(x):
        counts = x.value_counts()
        return counts.index[0]

    # API Metrics
    api_metrics = (
        df.groupby("api_name").agg(
            total_requests=("request_id", "count"),
            success_rate=("is_success", "mean"),
            avg_latency_ms=("latency_ms", "mean"),
            p95_latency_ms=("latency_ms", p95),
            top_error_reason=("error_reason", most_common_error)
        )
        .reset_index()
    )

    api_metrics["success_rate"] = (api_metrics["success_rate"] * 100).round(2)
    api_metrics["avg_latency_ms"] = api_metrics["avg_latency_ms"].round(2)
    api_metrics["p95_latency_ms"] = api_metrics["p95_latency_ms"].round(2)

    # Funnel Metrics
    funnel_metrics = (
        df.groupby("api_name")
        .agg(
            total_requests=("request_id", "count"),
            successful_requests=("is_success", "sum")
        )
        .reset_index()
    )
    funnel_metrics["conversion_rate"] = (
        funnel_metrics["successful_requests"] / funnel_metrics["total_requests"] * 100
    ).round(2)

    # Region Metrics
    region_metrics = (
        df.groupby("region")
        .agg(
            total_requests=("request_id", "count"),
            success_rate=("is_success", "mean")
        )
        .reset_index()
    )
    region_metrics["success_rate"] = (region_metrics["success_rate"] * 100).round(2)
    
    return api_metrics, funnel_metrics, region_metrics


def calculate_metrics_from_sql():
    """Calculate metrics using SQL queries from MySQL database"""
    print("🗄️  Using SQL/MySQL approach...")
    
    try:
        from sql_connector import get_api_metrics, get_funnel_metrics, get_region_metrics
        
        api_metrics = get_api_metrics()
        funnel_metrics = get_funnel_metrics()
        region_metrics = get_region_metrics()
        
        print("✓ Successfully fetched metrics from MySQL database")
        return api_metrics, funnel_metrics, region_metrics
    
    except ImportError:
        print("✗ Error: sql_connector module not found")
        raise
    except Exception as e:
        print(f"✗ Error fetching data from MySQL: {e}")
        print("💡 Tip: Check your database configuration in config.py")
        raise


def main():
    """Main execution function"""
    print("=" * 60)
    print("API Analytics - Metrics Aggregation")
    print("=" * 60)
    
    # Choose data source based on configuration
    if DATA_SOURCE.upper() == 'SQL':
        api_metrics, funnel_metrics, region_metrics = calculate_metrics_from_sql()
    elif DATA_SOURCE.upper() == 'CSV':
        api_metrics, funnel_metrics, region_metrics = calculate_metrics_from_csv()
    else:
        raise ValueError(f"Invalid DATA_SOURCE: {DATA_SOURCE}. Must be 'SQL' or 'CSV'")
    
    # Save results to CSV files
    api_metrics.to_csv(CSV_CONFIG['api_metrics_output'], index=False)
    funnel_metrics.to_csv(CSV_CONFIG['funnel_metrics_output'], index=False)
    region_metrics.to_csv(CSV_CONFIG['region_metrics_output'], index=False)
    
    print("\n✓ Metrics calculated successfully!")
    print(f"  - {CSV_CONFIG['api_metrics_output']}")
    print(f"  - {CSV_CONFIG['funnel_metrics_output']}")
    print(f"  - {CSV_CONFIG['region_metrics_output']}")
    print("=" * 60)


if __name__ == "__main__":
    main()

