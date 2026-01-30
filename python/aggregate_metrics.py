import pandas as pd
import numpy as np

df=pd.read_csv("../querypart/api_logs_myql.csv")
df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])
df["is_success"] = df["status_Code"] == 200

def p95(series):
    return np.percentile(series, 95)
def most_common_error(x):
    counts = x.value_counts()
    return counts.index[0]

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

region_metrics = (
    df.groupby("region")
    .agg(
        total_requests=("request_id", "count"),
        success_rate=("is_success", "mean")
    )
    .reset_index()
)
region_metrics["success_rate"] = (region_metrics["success_rate"] * 100).round(2)

api_metrics.to_csv("api_metrics.csv", index=False)
funnel_metrics.to_csv("funnel_metrics.csv", index=False)
region_metrics.to_csv("region_metrics.csv", index=False)

