import streamlit as st
import pandas as pd
import subprocess

st.set_page_config(page_title="API Performance Analytics", layout="wide")

# -----------------------------
# Load data
# -----------------------------
api_metrics = pd.read_csv("../python/api_metrics.csv")
funnel_metrics = pd.read_csv("../python/funnel_metrics.csv")
region_metrics = pd.read_csv("../python/region_metrics.csv")

# -----------------------------
# Title
# -----------------------------
st.title("📊 API Performance, Conversion & AI-Driven Insights")

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
