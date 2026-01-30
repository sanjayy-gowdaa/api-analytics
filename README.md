# 📊 API Analytics Dashboard for Product Analysts

> **AI-Powered Analytics Platform for FinTech API Performance & Conversion Optimization**

A comprehensive analytics solution designed specifically for Product Analysts working with API-driven products. This platform transforms raw API logs into actionable insights using data aggregation, visualization, and AI-powered recommendations to drive product decisions and improve conversion rates.

---

## 🎯 Overview

As a Product Analyst in a FinTech environment, understanding API performance and its impact on user conversion is critical. This project provides:

- **Performance Monitoring**: Track API latency, success rates, and error patterns
- **Conversion Analysis**: Understand how API performance affects user funnels
- **Regional Insights**: Identify geographic performance variations
- **AI-Powered Recommendations**: Get actionable product improvements from Gemini AI

---

## 🚀 Key Features

### 1. **API Performance Analytics**
Monitor critical API metrics that directly impact user experience:
- Request volume and success rates
- Average and P95 latency measurements
- Error reason identification and frequency
- API-by-API performance comparison

![API Performance Overview](pics/api.png)

### 2. **Conversion Funnel Analysis**
Understand the relationship between API performance and conversion:
- Request-to-success conversion rates
- Drop-off point identification
- API-specific conversion metrics

![Conversion Funnel](pics/conversion%20funnel.png)

### 3. **Regional Performance Insights**
Analyze geographic variations in API performance:
- Region-wise success rates
- Geographic bottleneck identification
- Infrastructure optimization opportunities

![Regional Analysis](pics/region.png)

### 4. **AI-Generated Product Insights**
Leverage Gemini AI for intelligent product recommendations:
- Root cause analysis of performance issues
- Impact assessment on user experience
- Concrete technical and product improvement suggestions
- Tailored recommendations for each API

![AI Insights](pics/ai_insight.png)

---

## 📁 Project Structure

```
api-analytics/
├── ai/                          # AI insights generation
│   └── insight_Ai.py           # Gemini AI integration for recommendations
├── dashboard/                   # Streamlit visualization
│   └── app.py                  # Interactive dashboard
├── python/                      # Data processing & aggregation
│   ├── aggregate_metrics.py    # Unified metrics calculator (CSV or SQL)
│   ├── sql_connector.py        # MySQL database connector
│   ├── config.py               # Configuration for data source selection
│   ├── api_metrics.csv         # Generated API metrics
│   ├── funnel_metrics.csv      # Generated conversion data
│   └── region_metrics.csv      # Generated regional data
├── querypart/                   # SQL queries & data source
│   ├── analysis.sql            # Production SQL queries
│   ├── query.sql               # Additional query examples
│   └── api_logs_myql.csv       # Raw API logs (CSV source)
├── generate/                    # Data generation utilities
│   ├── generatelogs.py         # Log generation script
│   └── raw_logs.csv            # Generated raw logs
└── pics/                        # Dashboard screenshots
```

---

## � Dual Implementation: SQL & Python

This project uniquely demonstrates **two approaches** to analytics, giving you flexibility based on your infrastructure:

### 🐍 Python/Pandas Approach (Default)
- Processes data from CSV files
- More flexible for complex transformations
- Better integration with ML/AI workflows
- Easier to iterate and prototype
- Perfect for exploratory analysis

### 🗄️ SQL/MySQL Approach
- Queries data directly from MySQL database
- Native database performance
- Faster for large datasets
- Production-ready for enterprise systems
- SQL queries available in `querypart/analysis.sql`

**Both approaches produce identical outputs** and work seamlessly with the Streamlit dashboard!

### Switching Between Approaches

Simply edit `python/config.py`:

```python
# Use CSV/Pandas
DATA_SOURCE = 'CSV'

# Or use SQL/MySQL
DATA_SOURCE = 'SQL'
```

---

## 🛠️ Technology Stack

- **Python 3.12**: Core programming language
- **Pandas & NumPy**: Data manipulation and statistical analysis
- **MySQL**: Database for SQL-based analytics
- **Streamlit**: Interactive dashboard framework
- **Google Gemini AI**: AI-powered insights generation

---

## 📋 Prerequisites

- Python 3.12 or higher
- Google Gemini API key (for AI insights)
- MySQL Server (optional, only for SQL approach)
- Required Python packages (see Installation)

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanjayy-gowdaa/api-analytics.git
   cd api-analytics
   ```

2. **Install dependencies**
   
   **For CSV/Pandas approach:**
   ```bash
   pip install pandas numpy streamlit google-generativeai python-dotenv
   ```
   
   **For SQL/MySQL approach (additional):**
   ```bash
   pip install mysql-connector-python
   ```

3. **Configure data source**
   
   Edit `python/config.py` to set your preferred data source:
   ```python
   # Choose 'CSV' or 'SQL'
   DATA_SOURCE = 'CSV'
   ```
   
   **If using SQL approach**, also configure database credentials:
   ```python
   DB_CONFIG = {
       'host': '127.0.0.1',
       'database': 'apidb',
       'user': 'your_username',
       'password': 'your_password'
   }
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Prepare your data**
   
   **For CSV approach:** Ensure API logs are in `querypart/api_logs_myql.csv`:
   ```csv
   request_id,api_name,TIMESTAMP,latency_ms,status_Code,document_type,region,device_type,error_reason
   ```
   
   **For SQL approach:** Load data into MySQL `api_logs` table with the same schema.

---

## 🚀 Usage

### Step 1: Generate Aggregated Metrics

Run the metrics aggregation script:

```bash
cd python
python aggregate_metrics.py
```

The script will automatically use your configured data source (CSV or SQL) and generate three CSV files:
- `api_metrics.csv`: API performance metrics
- `funnel_metrics.csv`: Conversion funnel data
- `region_metrics.csv`: Regional performance data

**Output example:**
```
============================================================
API Analytics - Metrics Aggregation
============================================================
📊 Using CSV/Pandas approach...
✓ Metrics calculated successfully!
  - api_metrics.csv
  - funnel_metrics.csv
  - region_metrics.csv
============================================================
```

### Step 2: Launch the Dashboard

Start the Streamlit dashboard:

```bash
cd dashboard
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Step 3: Generate AI Insights

1. Select an API from the dropdown menu
2. Click "Generate Improvement Suggestions"
3. Review AI-powered recommendations for product improvements

---

## 📊 Metrics Calculated

### API Performance Metrics
- **Total Requests**: Volume of API calls
- **Success Rate**: Percentage of successful requests (status code 200)
- **Average Latency**: Mean response time in milliseconds
- **P95 Latency**: 95th percentile latency (performance consistency)
- **Top Error Reason**: Most common failure cause

### Conversion Metrics
- **Conversion Rate**: Percentage of successful requests per API
- **Successful Requests**: Count of successful calls
- **Drop-off Analysis**: Failed request patterns

### Regional Metrics
- **Success Rate by Region**: Geographic performance variations
- **Request Distribution**: Regional traffic patterns

---

## 🔄 SQL vs Python: When to Use Each

### Use **Python/Pandas** When:
- ✅ Prototyping and exploratory data analysis
- ✅ Complex data transformations not easily done in SQL
- ✅ Integrating with ML/AI models (like Gemini)
- ✅ Working with multiple data sources (APIs, files, databases)
- ✅ Need for rapid iteration and experimentation
- ✅ Team has stronger Python skills

### Use **SQL/MySQL** When:
- ✅ Data already lives in a database
- ✅ Working with large datasets (10M+ rows)
- ✅ Need production-grade performance
- ✅ Multiple teams need access to the same metrics
- ✅ Enterprise infrastructure with existing MySQL setup
- ✅ Team has strong SQL/database expertise

### Performance Comparison

| Metric | CSV/Pandas | SQL/MySQL |
|--------|-----------|-----------|
| **Setup Time** | Fast (no DB needed) | Slower (DB setup required) |
| **Small Datasets (<100K rows)** | Fast | Fast |
| **Large Datasets (1M+ rows)** | Slower | Much Faster |
| **Flexibility** | Very High | Moderate |
| **Maintenance** | Low | Requires DB admin |
| **Scalability** | Limited by memory | High |

**Pro Tip**: Start with CSV/Pandas for prototyping, then switch to SQL/MySQL for production deployment!

---

## 🤖 AI Insights Features

The AI-powered insights module provides:

1. **Root Cause Analysis**: Identifies likely causes of performance degradation or conversion issues
2. **Impact Assessment**: Evaluates effects on user experience and business metrics
3. **Actionable Recommendations**: Provides 2-3 concrete technical or product improvements
4. **Context-Aware Suggestions**: Tailored to each API's specific metrics and failure patterns

---

## 📈 Use Cases for Product Analysts

### 1. **Performance Optimization**
- Identify slow APIs impacting user experience
- Prioritize optimization efforts based on P95 latency
- Track performance improvements over time

### 2. **Conversion Rate Optimization**
- Correlate API failures with conversion drops
- Identify friction points in user journeys
- A/B test API improvements impact

### 3. **Product Roadmap Planning**
- Use AI recommendations for feature prioritization
- Data-driven decision making for technical debt
- Resource allocation based on impact analysis

### 4. **Stakeholder Communication**
- Visual dashboards for executive presentations
- Clear metrics for engineering team alignment
- ROI justification for infrastructure investments

---

## 🔧 Customization

### Modify Metrics Calculations

Edit `python/aggregate_metrics.py` to add custom metrics:

```python
# Example: Add median latency
api_metrics = df.groupby("api_name").agg(
    median_latency=("latency_ms", "median")
)
```

### Customize AI Prompts

Edit `ai/insight_Ai.py` to adjust AI analysis focus:

```python
prompt = f"""
Your custom prompt here with {row['api_name']} metrics...
"""
```

### Extend Dashboard Visualizations

Edit `dashboard/app.py` to add new charts or sections:

```python
st.header("Your Custom Analysis")
st.line_chart(your_data)
```

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Sanjay Gowda**
- GitHub: [@sanjayy-gowdaa](https://github.com/sanjayy-gowdaa)

---
