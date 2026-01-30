import os
import sys
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

df = pd.read_csv("../python/api_metrics.csv")

# Get API name from command line argument, default to first row if not provided
if len(sys.argv) > 1:
    api_name = sys.argv[1]
    row = df[df['api_name'] == api_name].iloc[0]
else:
    row = df.iloc[0]
prompt = f"""
You are a Product Analyst at a fintech company.

Given the following API performance metrics:

API Name: {row['api_name']}
Total Requests: {row['total_requests']}
Success Rate: {row['success_rate']}%
Average Latency: {row['avg_latency_ms']} ms
P95 Latency: {row['p95_latency_ms']} ms
Top Failure Reason: {row['top_error_reason']}

Answer in bullet points:
1. Likely root cause of performance or conversion issues
2. Impact on user experience or conversion
3. 2–3 concrete technical or product improvements
Keep it concise and actionable.
"""
response = model.generate_content(prompt)

print("\n Insights:\n")
print(response.text)
