from pathlib import Path
import os
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

# Path configurations
RAW_DATA_PATH = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
SCHEMA_PATH = Path("sql/schema.sql")
DATABASE_PATH = Path("bluestock_mf.db")

# Ensure processed directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("=" * 70)
print("BLUESTOCK MUTUAL FUND CAPSTONE - DATA INGESTION & PIPELINE ENGINE")
print("=" * 70)

# ----------------------------------------------------------------
# STEP 1: INITIALIZE DATABASE SCHEMA
# ----------------------------------------------------------------
print("\n  Step 1: Building database tables from sql/schema.sql...")
if not SCHEMA_PATH.exists():
    print(f" Error: Cannot find schema file at {SCHEMA_PATH}")
    exit(1)

with open(SCHEMA_PATH, "r") as f:
    schema_sql = f.read()

with sqlite3.connect(DATABASE_PATH) as conn:
    conn.executescript(schema_sql)
print(" Relational tables initialized successfully.")

# Initialize SQLAlchemy Engine connection for pandas loading
engine = create_engine(f"sqlite:///{DATABASE_PATH}")

# ----------------------------------------------------------------
# STEP 2: GENERATE DATE DIMENSION DYNAMICALLY
# ----------------------------------------------------------------
print("\n Step 2: Injecting Date Dimension matrix (2021-2026)...")
date_range = pd.date_range(start="2021-01-01", end="2026-12-31", freq="D")
dim_date_df = pd.DataFrame(
    {
        "date_id": date_range.strftime("%Y-%m-%d"),
        "calendar_year": date_range.year,
        "calendar_month": date_range.month,
        "calendar_day": date_range.day,
        "day_of_week": date_range.day_name(),
        "is_weekend": date_range.weekday.map(lambda x: 1 if x >= 5 else 0),
    }
)
dim_date_df.to_sql("dim_date", engine, if_exists="append", index=False)
print("Date dimension loaded.")

# ----------------------------------------------------------------
# STEP 3: INSPECT, CLEAN, AND INGEST ALL RAW DATASETS
# ----------------------------------------------------------------
print("\n Step 3: Scanning data profiles, running pipeline transformations...")

csv_files = sorted(RAW_DATA_PATH.glob("*.csv"))

# Dictionary mappings to build dim_fund iteratively
funds_master_list = []
performance_master_list = []

for file in csv_files:
    print("\n" + "=" * 70)
    print(f"Dataset: {file.name}")
    print("=" * 70)

    try:
        df = pd.read_csv(file)

        # Keep your original inspection console outputs
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Missing Values:\n{df.isnull().sum()}")
        print(f"Duplicate Rows: {df.duplicated().sum()}")
        print(
            f"Memory Usage (MB): {round(df.memory_usage(deep=True).sum() / 1024**2, 2)}"
        )

        # --------------------------------------------------------
        # CUSTOM TRANSLATION AND TARGET FACT LOADING LOGIC
        # --------------------------------------------------------

        # 1. Handle nav_history
        if "02_nav_history" in file.name:
            print("   Cleaning & Loading nav history into 'fact_nav'...")
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.dropna(subset=["date"])
            df = df.drop_duplicates(subset=["amfi_code", "date"])
            df = df[df["nav"] > 0]
            df = df.sort_values(by=["amfi_code", "date"])
            df.set_index("date", inplace=True)
            df = df.groupby("amfi_code").resample("D").ffill()
            if "amfi_code" in df.columns:
                df = df.drop(columns=["amfi_code"])
            df = df.reset_index().rename(columns={"date": "date_id"})

            df[["amfi_code", "date_id", "nav"]].to_sql(
                "fact_nav", engine, if_exists="append", index=False
            )
            df.to_csv(PROCESSED_DIR / "cleaned_nav_history.csv", index=False)

        # 2. Handle investor_transactions
        elif "08_investor_transactions" in file.name:
            print("   Cleaning & Loading transactions into 'fact_transactions'...")
            df["transaction_date"] = pd.to_datetime(
                df["transaction_date"], errors="coerce"
            ).dt.strftime("%Y-%m-%d")
            df = df.dropna(subset=["transaction_date"])
            df["transaction_type"] = (
                df["transaction_type"].astype(str).str.strip().str.upper()
            )
            type_mapping = {
                "SIP": "SIP",
                "LUMPSUM": "Lumpsum",
                "REDEMPTION": "Redemption",
            }
            df["transaction_type"] = df["transaction_type"].map(
                lambda x: type_mapping.get(x, "Lumpsum")
            )
            df = df[df["amount_inr"] > 0]
            df["kyc_status"] = df["kyc_status"].astype(str).str.strip().str.capitalize()
            df["kyc_status"] = df["kyc_status"].apply(
                lambda x: x if x in ["Verified", "Pending", "Failed"] else "Pending"
            )

            trans_cols = [
                "investor_id",
                "transaction_date",
                "amfi_code",
                "transaction_type",
                "amount_inr",
                "state",
                "city",
                "city_tier",
                "age_group",
                "gender",
                "annual_income_lakh",
                "payment_mode",
                "kyc_status",
            ]
            df[trans_cols].to_sql(
                "fact_transactions", engine, if_exists="append", index=False
            )
            df.to_csv(PROCESSED_DIR / "cleaned_investor_transactions.csv", index=False)

        # 3. Handle scheme_performance
        elif "07_scheme_performance" in file.name:
            print(
                "   Cleaning & Loading performance metadata into 'fact_performance'..."
            )
            for col in [
                "return_1yr_pct",
                "return_3yr_pct",
                "return_5yr_pct",
                "benchmark_3yr_pct",
            ]:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
            df["expense_ratio_pct"] = pd.to_numeric(
                df["expense_ratio_pct"], errors="coerce"
            )
            df["expense_anomaly_flag"] = np.where(
                (df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5), 1, 0
            )

            # Cache metadata for dim_fund merge
            performance_master_list.append(
                df[["amfi_code", "scheme_name", "fund_house", "category", "plan"]]
            )

            perf_cols = [
                "amfi_code",
                "return_1yr_pct",
                "return_3yr_pct",
                "return_5yr_pct",
                "benchmark_3yr_pct",
                "alpha",
                "beta",
                "sharpe_ratio",
                "sortino_ratio",
                "expense_ratio_pct",
                "expense_anomaly_flag",
                "morningstar_rating",
                "risk_grade",
            ]
            df[perf_cols].to_sql(
                "fact_performance", engine, if_exists="append", index=False
            )
            df.to_csv(PROCESSED_DIR / "cleaned_scheme_performance.csv", index=False)

        # 4. Handle aum_by_fund_house (LOOSENED STRING MATCH FOR SAFE ACQUISITION)
        elif "03_aum_by_fund_house" in file.name:
            print("   Loading AUM data rows into 'fact_aum'...")
            df_aum = df.rename(columns={"date": "date_id"})
            df_aum[["date_id", "fund_house", "aum_crore", "num_schemes"]].to_sql(
                "fact_aum", engine, if_exists="append", index=False
            )
            df.to_csv(PROCESSED_DIR / "cleaned_aum_by_fund_house.csv", index=False)

        # 5. Handle monthly_sip_inflows
        elif "04_monthly_sip_inflows" in file.name:
            print("   Loading SIP structural rows into 'tracking_sip_inflows'...")
            df["yoy_growth_pct"] = df["yoy_growth_pct"].fillna(0.0)
            sip_cols = [
                "month",
                "sip_inflow_crore",
                "active_sip_accounts_crore",
                "new_sip_accounts_lakh",
                "sip_aum_lakh_crore",
                "yoy_growth_pct",
            ]
            df[sip_cols].to_sql(
                "tracking_sip_inflows", engine, if_exists="append", index=False
            )
            df.to_csv(PROCESSED_DIR / "cleaned_monthly_sip_inflows.csv", index=False)

        # Cache funds master profiles if found
        if "01_fund_master" in file.name:
            print("   Caching Fund Masters for Dim Fund orchestration...")
            funds_master_list.append(
                df[
                    [
                        "amfi_code",
                        "scheme_name",
                        "fund_house",
                        "category",
                        "plan",
                        "risk_category",
                        "sebi_category_code",
                    ]
                ]
            )
            df.to_csv(PROCESSED_DIR / "cleaned_mutual_funds.csv", index=False)

        # Passive clean export handler to preserve strict 10-file processed structure
        if "05_category_inflows" in file.name:
            df.to_csv(PROCESSED_DIR / "cleaned_category_inflows.csv", index=False)
        elif "06_industry_folio_count" in file.name:
            df.to_csv(PROCESSED_DIR / "cleaned_industry_folio_count.csv", index=False)
        elif "09_portfolio_holdings" in file.name:
            df.to_csv(PROCESSED_DIR / "cleaned_portfolio_holdings.csv", index=False)
        elif "10_benchmark_indices" in file.name:
            df.to_csv(PROCESSED_DIR / "cleaned_benchmark_indices.csv", index=False)
        elif "live_nav" in file.name:
            df.to_csv(PROCESSED_DIR / "cleaned_live_nav.csv", index=False)

    except Exception as e:
        print(f" Error processing dataset {file.name}: {e}")

# ----------------------------------------------------------------
# STEP 4: MERGE AND POPULATE FUND DIMENSION (dim_fund)
# ----------------------------------------------------------------
print("\n📑 Step 4: Constructing unified 'dim_fund' dimension mapping...")
try:
    f_df = pd.concat(funds_master_list) if funds_master_list else pd.DataFrame()
    p_df = (
        pd.concat(performance_master_list)
        if performance_master_list
        else pd.DataFrame()
    )

    if not p_df.empty and not f_df.empty:
        p_df = p_df.assign(risk_category="Unknown", sebi_category_code="Unknown")
        dim_fund_df = pd.concat([f_df, p_df]).drop_duplicates(subset=["amfi_code"])
    elif not f_df.empty:
        dim_fund_df = f_df.drop_duplicates(subset=["amfi_code"])
    else:
        dim_fund_df = p_df.assign(
            risk_category="Unknown", sebi_category_code="Unknown"
        ).drop_duplicates(subset=["amfi_code"])

    dim_fund_df.to_sql("dim_fund", engine, if_exists="append", index=False)
    print(f"Successfully written fund profiles to 'dim_fund'.")
except Exception as e:
    print(f" Warning during Dim Fund assembly execution: {e}")

# ----------------------------------------------------------------
# STEP 5: INTEGRITY COUNT CHECK REPORT
# ----------------------------------------------------------------
print("\n" + "=" * 70)
print(" DB LOAD COMPLETED — RUNNING RECORD COUNT INTEGRITY CHECK")
print("=" * 70)
with sqlite3.connect(DATABASE_PATH) as conn:
    cursor = conn.cursor()
    target_tables = [
        "dim_fund",
        "dim_date",
        "fact_nav",
        "fact_transactions",
        "fact_performance",
        "fact_aum",
        "tracking_sip_inflows",
    ]
    for table in target_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f" Database Table '{table}': {cursor.fetchone()[0]} rows validated.")

print("\n" + "=" * 70)
print(" ALL REQ DATA INGESTION & PIPELINE STACKS COMPLETED!")
print("=" * 70)
