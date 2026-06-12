# 📈 Bluestock Mutual Fund Analytics Platform

### End-to-End Financial Analytics, Risk Assessment & Investor Intelligence System

An enterprise-style Mutual Fund Analytics Platform developed as part of the Bluestock Fintech Capstone Project. The platform combines Data Engineering, Financial Analytics, Risk Modeling, and Business Intelligence to transform raw mutual fund datasets into actionable insights for investors, analysts, and fund managers.

---

# 🚀 Project Overview

The mutual fund industry generates large volumes of data across fund performance, investor transactions, benchmark indices, portfolio holdings, Assets Under Management (AUM), and SIP inflows. Extracting meaningful insights from these datasets requires robust data pipelines, analytical frameworks, and visualization tools.

This project addresses these challenges by building a complete analytics ecosystem capable of:

* Processing and transforming raw mutual fund datasets
* Measuring fund performance using financial metrics
* Evaluating investor participation patterns
* Performing advanced risk analysis
* Measuring portfolio diversification
* Generating investment recommendations
* Delivering insights through interactive dashboards

---

# 📌 Project Statistics

| Metric                        | Value          |
| ----------------------------- | -------------- |
| Total Records Processed       | 100,000+       |
| Mutual Funds Analyzed         | 40             |
| Investors Analyzed            | 5,000          |
| Portfolio Funds Analyzed      | 34             |
| NAV Records Processed         | 64,320         |
| Transaction Records Processed | 32,778         |
| Analysis Period               | 2021 – 2026    |
| Database Tables               | 7 Core Tables  |
| Data Quality                  | 100% Validated |

---

# 🎯 Business Objectives

### Objective 1

Develop a robust ETL pipeline for mutual fund datasets.

### Objective 2

Analyze historical mutual fund performance and benchmark trends.

### Objective 3

Study investor participation, SIP behavior, and demographic patterns.

### Objective 4

Measure portfolio diversification and sector concentration.

### Objective 5

Compute advanced risk metrics including VaR and CVaR.

### Objective 6

Track risk-adjusted performance using Rolling Sharpe Ratio analysis.

### Objective 7

Build a personalized mutual fund recommendation engine.

### Objective 8

Provide business-ready insights through an analytics dashboard.

---

# ⭐ Key Highlights

✅ Built a complete end-to-end ETL pipeline

✅ Processed and analyzed over 100,000 financial records

✅ Evaluated 40 mutual fund schemes and 5,000 investors

✅ Computed CAGR, Sharpe Ratio, Sortino Ratio, Alpha, Beta and Maximum Drawdown

✅ Implemented Historical VaR and CVaR Risk Analytics

✅ Performed Rolling 90-Day Sharpe Ratio Analysis

✅ Conducted Investor Cohort and SIP Continuity Analysis

✅ Measured Portfolio Concentration using HHI

✅ Developed a Rule-Based Mutual Fund Recommendation Engine

✅ Built an Interactive Analytics Dashboard

---

# 🛠 Technology Stack

## Programming

* Python

## Data Processing

* Pandas
* NumPy

## Financial Analytics

* SciPy
* Statistical Risk Models

## Visualization

* Matplotlib
* Plotly

## Database

* SQLite

## Dashboard & Business Intelligence

* Power BI
* Streamlit

## Development Tools

* Git
* GitHub
* VS Code
* Jupyter Notebook

---

# 🏗 Project Architecture

```text
Raw Data Sources
        │
        ▼
Data Ingestion Layer
        │
        ▼
ETL Pipeline
        │
        ▼
Processed Data Layer
        │
        ▼
SQLite Database
        │
        ▼
Analytics Engine
        │
        ▼
Risk Models & Recommendations
        │
        ▼
Dashboard & Reports
        │
        ▼
Business Insights
```

---

# 📂 Project Structure

```text
BLUESTOCK_MF_CAPSTONE
│
├── Advance_Analytics
│   ├── Advanced_Analytics.ipynb
│   ├── recommender.py
│   ├── rolling_sharpe_chart.png
│   └── var_cvar_report.csv
│
├── dashboard
│   ├── dashboard_app_work.py
│   ├── Bluestock_Fintech.pbit
│   └── Dashboard.pdf
│
├── data
│   ├── raw
│   ├── processed
│   └── db
│
├── notebooks
│   ├── EDA_Analysis.ipynb
│   └── Performance_Analytics.ipynb
│
├── reports
│   ├── Final_Report.pdf
│   ├── Bluestock_MF_Presentation.pptx
│   └── exported_charts
│
├── scripts
│   ├── data_ingestion.py
│   └── etl_pipeline.py
│
├── sql
│   ├── schema.sql
│   ├── queries.sql
│   └── data_dictionary.md
│
├── requirements.txt
└── README.md
```

---

# 📊 Data Sources

The platform integrates multiple datasets representing different dimensions of the mutual fund ecosystem.

### Mutual Fund Master Data

* Fund House Information
* Scheme Metadata
* Category Mapping
* Benchmark Details

### NAV History

* Daily NAV Values
* Historical Returns
* Performance Trends

### Portfolio Holdings

* Sector Allocation
* Portfolio Composition
* Market Exposure

### Investor Transactions

* SIP Transactions
* Redemption Activity
* Investor Participation

### Benchmark Data

* Market Index Tracking
* Comparative Performance Analysis

---

# ⚙ ETL Pipeline

The ETL layer automates the preparation of raw datasets for analytical processing.

## Extract

* Load source datasets
* Validate schema consistency
* Verify AMFI mappings

## Transform

* Missing value handling
* Data standardization
* Feature engineering
* Aggregation and validation

## Load

* Populate SQLite database
* Generate analytical datasets
* Create reporting outputs

### Execute Pipeline

```bash
python scripts/etl_pipeline.py
```

---

# 📈 Exploratory Data Analysis

The EDA module investigates key trends across the mutual fund ecosystem.

### Analysis Performed

* Benchmark Comparison Analysis
* AUM Growth Analysis
* SIP Inflow Trends
* Category Inflow Analysis
* Investor Demographic Analysis
* Geographic Distribution Analysis
* NAV Correlation Analysis
* Portfolio Allocation Analysis

---

# 📉 Advanced Analytics

## Performance Analytics

Metrics computed for all mutual fund schemes:

* CAGR
* Sharpe Ratio
* Sortino Ratio
* Alpha
* Beta
* Maximum Drawdown
* Composite Fund Score

### Deliverables

* fund_scorecard.csv
* alpha_beta.csv

---

## Historical VaR & CVaR

Evaluates downside and tail-risk exposure at a 95% confidence level.

### Deliverable

* var_cvar_report.csv

---

## Rolling 90-Day Sharpe Ratio

Measures changing risk-adjusted performance through time.

### Deliverable

* rolling_sharpe_chart.png

---

## Investor Cohort Analysis

Evaluates investor behavior by first transaction year.

Metrics include:

* Average SIP Amount
* Total Investment
* Preferred Fund Selection

---

## SIP Continuity Analysis

Identifies investors with irregular SIP behavior and potential churn risk.

Metrics include:

* Average SIP Gap
* Continuity Rate
* At-Risk Investors

---

## Sector Concentration Analysis (HHI)

Measures portfolio diversification using the Herfindahl-Hirschman Index.

Identifies:

* Highly Concentrated Funds
* Diversified Funds
* Sector Exposure Risk

---

# 🤖 Mutual Fund Recommendation Engine

A rule-based recommendation engine developed using fund performance metrics.

### Inputs

* Low Risk
* Moderate Risk
* High Risk

### Outputs

* Top 3 Recommended Funds
* Sharpe Ratio
* CAGR
* Alpha
* Fund Score

---

# 📊 Dashboard Features

The analytics dashboard provides:

* Fund Performance Monitoring
* Benchmark Comparison
* Investor Analytics
* Risk Analytics
* Portfolio Analysis
* SIP Trend Analysis
* Interactive Visualizations

---

# 🔍 Key Insights Generated

* Highest Fund Score: 91.63
* Average Portfolio HHI: 0.204
* Most Concentrated Portfolio HHI: 0.297
* Most Diversified Portfolio HHI: 0.124
* Highest Risk Fund (VaR): AMFI 101207
* Lowest Risk Fund (VaR): AMFI 100025
* 2024 Investor Cohort Investment: ₹349.1 Crore
* SIP Continuity Rate: 2.2%
* Significant variation observed across risk-adjusted performance metrics

---

# 💼 Skills Demonstrated

* Data Engineering
* ETL Pipeline Development
* Financial Analytics
* Risk Modeling
* SQL Database Design
* Business Intelligence
* Dashboard Development
* Data Visualization
* Investor Analytics
* Recommendation Systems

---

# ▶ How to Run the Project

## Clone Repository

```bash
git clone <repository-url>
cd BLUESTOCK_MF_CAPSTONE
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run ETL Pipeline

```bash
python scripts/etl_pipeline.py
```

## Launch Dashboard

```bash
streamlit run dashboard/dashboard_app_work.py
```

---

# 📦 Deliverables

## Day 1 Deliverables

* data_ingestion.py
* live_nav_fetch.py
* requirements.txt

## Day 2–4 Deliverables

* EDA_Analysis.ipynb
* Performance_Analytics.ipynb
* fund_scorecard.csv
* alpha_beta.csv

## Day 5 Deliverables

* Dashboard.pbix
* Dashboard.pdf

## Day 6 Deliverables

* Advanced_Analytics.ipynb
* recommender.py
* rolling_sharpe_chart.png
* var_cvar_report.csv

## Final Deliverables

* Final_Report.pdf
* Bluestock_MF_Presentation.pptx
* GitHub Repository

---

# 🔮 Future Enhancements

* Machine Learning-Based Fund Recommendation System
* Real-Time NAV Integration
* Portfolio Optimization Models
* Investor Churn Prediction
* Automated Risk Monitoring
* Cloud Deployment & Dashboard Hosting

---

# 👩‍💻 Author

**Minakshi Kaushik**

B.Tech Computer Science Engineering

Indira Gandhi Delhi Technical University for Women (IGDTUW)

Areas of Interest:

* Data Analytics
* FinTech
* Machine Learning
* Business Intelligence
* Financial Data Science

---

# 📜 License

This project was developed for academic and educational purposes as part of the Bluestock Fintech Internship Capstone Project.
## Live Demo

https://bluestock-mutualfund-capstone-8ct6n8tijzlpim2wyf9wtx.streamlit.app/