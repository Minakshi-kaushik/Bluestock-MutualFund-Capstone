import os
import pandas as pd
import numpy as np

# Ensure target directory exists for clean outputs
os.makedirs("data/processed", exist_ok=True)

# Define the base paths exactly matching your workspace structure
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


def clean_nav_history():
    print(" Cleaning nav_history.csv...")
    raw_path = os.path.join(RAW_DIR, "02_nav_history.csv")
    if not os.path.exists(raw_path):
        print(f" Error: Could not find 02_nav_history.csv in {RAW_DIR}")
        return None

    df = pd.read_csv(raw_path)

    # Parse dates and handle formatting anomalies
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Remove duplicates
    df = df.drop_duplicates(subset=["amfi_code", "date"])

    # Validation: NAV must be positive
    df = df[df["nav"] > 0]

    # Forward-fill missing dates for holidays/weekends per fund group
    df = df.sort_values(by=["amfi_code", "date"])

    df.set_index("date", inplace=True)
    # Added include_groups=False to silence the future warning neatly!
    df = df.groupby("amfi_code").resample("D").ffill()
    if "amfi_code" in df.columns:
        df = df.drop(columns=["amfi_code"])
    df = df.reset_index()

    output_path = os.path.join(PROCESSED_DIR, "cleaned_nav_history.csv")
    df.to_csv(output_path, index=False)
    print(" Successfully processed nav_history.csv")
    return df


def clean_investor_transactions():
    print("🧼 Cleaning investor_transactions.csv...")
    raw_path = os.path.join(RAW_DIR, "08_investor_transactions.csv")
    if not os.path.exists(raw_path):
        print(f" Error: Could not find 08_investor_transactions.csv in {RAW_DIR}")
        return None

    df = pd.read_csv(raw_path)

    # Fix and standardize dates
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df = df.dropna(subset=["transaction_date"])

    # Standardize Transaction Type Enum
    df["transaction_type"] = df["transaction_type"].astype(str).str.strip().str.upper()
    type_mapping = {"SIP": "SIP", "LUMPSUM": "Lumpsum", "REDEMPTION": "Redemption"}
    df["transaction_type"] = df["transaction_type"].map(
        lambda x: type_mapping.get(x, "Lumpsum")
    )

    # Validate financial constraints
    df = df[df["amount_inr"] > 0]

    # Standardize KYC Status Enum Values
    df["kyc_status"] = df["kyc_status"].astype(str).str.strip().str.capitalize()
    valid_kyc = ["Verified", "Pending", "Failed"]
    df["kyc_status"] = df["kyc_status"].apply(
        lambda x: x if x in valid_kyc else "Pending"
    )

    output_path = os.path.join(PROCESSED_DIR, "cleaned_investor_transactions.csv")
    df.to_csv(output_path, index=False)
    print("Successfully processed investor_transactions.csv")
    return df


def clean_scheme_performance():
    print("🧼 Cleaning scheme_performance.csv...")
    raw_path = os.path.join(RAW_DIR, "07_scheme_performance.csv")
    if not os.path.exists(raw_path):
        print(f" Error: Could not find 07_scheme_performance.csv in {RAW_DIR}")
        return None

    df = pd.read_csv(raw_path)

    # Coerce return columns to numeric types
    return_cols = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
    ]
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    # Standardize and constraint check expense ratios
    df["expense_ratio_pct"] = pd.to_numeric(df["expense_ratio_pct"], errors="coerce")
    # Flag expense anomalies outside expected ranges (0.1% - 2.5%)
    df["expense_anomaly_flag"] = np.where(
        (df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5), 1, 0
    )

    output_path = os.path.join(PROCESSED_DIR, "cleaned_scheme_performance.csv")
    df.to_csv(output_path, index=False)
    print(" Successfully processed scheme_performance.csv")
    return df


def process_remaining_files():
    print("🚀 Saving auxiliary tracking files to processed directory...")

    file_mappings = [
        ("01_fund_master.csv", "cleaned_mutual_funds.csv"),
        ("03_aum_by_fund_house (1).csv", "cleaned_aum_by_fund_house.csv"),
        ("04_monthly_sip_inflows.csv", "cleaned_monthly_sip_inflows.csv"),
        ("05_category_inflows.csv", "cleaned_category_inflows.csv"),
        ("06_industry_folio_count.csv", "cleaned_industry_folio_count.csv"),
        ("09_portfolio_holdings.csv", "cleaned_portfolio_holdings.csv"),
        ("10_benchmark_indices.csv", "cleaned_benchmark_indices.csv"),
        ("Axis_Bluechip_live_nav.csv", "cleaned_Axis_Bluechip_live_nav.csv"),
        (
            "HDFC_Top_100_Direct_live_nav.csv",
            "cleaned_HDFC_Top_100_Direct_live_nav.csv",
        ),
        ("ICICI_Bluechip_live_nav.csv", "cleaned_ICICI_Bluechip_live_nav.csv"),
        ("Kotak_Bluechip_live_nav.csv", "cleaned_Kotak_Bluechip_live_nav.csv"),
        ("Nippon_Large_Cap_live_nav.csv", "cleaned_Nippon_Large_Cap_live_nav.csv"),
        ("SBI_Bluechip_live_nav.csv", "cleaned_SBI_Bluechip_live_nav.csv"),
    ]

    for file_name, out_name in file_mappings:
        raw_path = os.path.join(RAW_DIR, file_name)
        if os.path.exists(raw_path):
            df = pd.read_csv(raw_path)

            if "yoy_growth_pct" in df.columns:
                df["yoy_growth_pct"] = df["yoy_growth_pct"].fillna(0.0)

            output_path = os.path.join(PROCESSED_DIR, out_name)
            df.to_csv(output_path, index=False)
        else:
            print(f" Warning: {file_name} not found in {RAW_DIR}")


if __name__ == "__main__":
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    process_remaining_files()
    print(
        "\n All datasets fully sanitized from data/raw/ and cleanly output to data/processed/!"
    )
