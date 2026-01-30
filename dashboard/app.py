import streamlit as st
import pandas as pd
import subprocess
import numpy as np
from io import StringIO

st.set_page_config(page_title="API Performance Analytics", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("📊 API Performance, Conversion & AI-Driven Insights")

# -----------------------------
# File Upload Section
# -----------------------------
st.sidebar.header("📂 Data Source")
upload_option = st.sidebar.radio(
    "Choose data source:",
    ["Use Pre-calculated Metrics", "Upload Raw Logs & Calculate"]
)

api_metrics = None
funnel_metrics = None
region_metrics = None

if upload_option == "Upload Raw Logs & Calculate":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Upload API Logs")
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV file with API logs",
        type=['csv'],
        help="CSV should have columns: request_id, api_name, TIMESTAMP, latency_ms, status_Code, error_reason, region"
    )
    
    if uploaded_file is not None:
        with st.spinner("📊 Processing uploaded file and calculating metrics..."):
            # Read uploaded file
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_cols = ['request_id', 'api_name', 'latency_ms', 'status_Code', 'error_reason', 'region']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                st.stop()
            
            # Calculate metrics
            df["is_success"] = df["status_Code"] == 200
            
            def p95(series):
                return np.percentile(series, 95)
            
            def most_common_error(x):
                counts = x.value_counts()
                return counts.index[0] if len(counts) > 0 else ''
            
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
            
            st.sidebar.success("✅ Metrics calculated successfully!")
    else:
        st.info("👈 Please upload a CSV file from the sidebar to calculate metrics")
        st.stop()

else:
    # Load pre-calculated data
    try:
        api_metrics = pd.read_csv("../python/api_metrics.csv")
        funnel_metrics = pd.read_csv("../python/funnel_metrics.csv")
        region_metrics = pd.read_csv("../python/region_metrics.csv")
    except FileNotFoundError as e:
        st.error(f"❌ Error loading pre-calculated metrics: {e}")
        st.info("💡 Tip: Run `python aggregate_metrics.py` in the python folder first, or use the upload option.")
        st.stop()

# -----------------------------
# API Overview
# -----------------------------
st.header("🔍 API Performance Overview")
st.dataframe(api_metrics)

st.subheader("Latency Comparison")
st.bar_chart(
    api_metrics.set_index("api_name")[["avg_latency_ms", "p95_latency_ms"]]
)

# -----------------------------
# Conversion Funnel
# -----------------------------
st.header("📉 Conversion Funnel")
st.dataframe(funnel_metrics)

st.bar_chart(
    funnel_metrics.set_index("api_name")[["conversion_rate"]]
)

# -----------------------------
# Region Performance
# -----------------------------
st.header("🌍 Region-wise Success Rate")
st.dataframe(region_metrics)

st.bar_chart(
    region_metrics.set_index("region")[["success_rate"]]
)

# -----------------------------
# Gemini Insights Section
# -----------------------------
st.header("🤖 AI-Generated Product Insights")

selected_api = st.selectbox(
    "Select API for Insight Generation",
    api_metrics["api_name"].unique()
)

if st.button("Generate Improvement Suggestions"):
    with st.spinner("Analyzing metrics with AI..."):
        result = subprocess.run(
            ["python", "../ai/insight_Ai.py", selected_api],
            capture_output=True,
            text=True
        )
        st.markdown(result.stdout)
