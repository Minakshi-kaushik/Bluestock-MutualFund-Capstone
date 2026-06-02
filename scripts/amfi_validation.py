from pathlib import Path
import pandas as pd

# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw"

fund_master_file = RAW_DATA_PATH / "01_fund_master.csv"
nav_history_file = RAW_DATA_PATH / "02_nav_history.csv"

# -----------------------------
# Load Datasets
# -----------------------------
print("=" * 70)
print("AMFI CODE VALIDATION")
print("=" * 70)

fund_master = pd.read_csv(fund_master_file)
nav_history = pd.read_csv(nav_history_file)

# -----------------------------
# Unique AMFI Codes
# -----------------------------
master_codes = set(fund_master["amfi_code"].unique())
nav_codes = set(nav_history["amfi_code"].unique())

print(f"\nTotal AMFI Codes in Fund Master : {len(master_codes)}")
print(f"Total AMFI Codes in NAV History : {len(nav_codes)}")

# -----------------------------
# Missing Codes
# -----------------------------
missing_in_nav = master_codes - nav_codes
extra_in_nav = nav_codes - master_codes

print("\n" + "=" * 70)
print("VALIDATION RESULTS")
print("=" * 70)

print(f"\nMissing Codes in NAV History : {len(missing_in_nav)}")
print(f"Extra Codes in NAV History   : {len(extra_in_nav)}")

# -----------------------------
# Missing Code Details
# -----------------------------
if len(missing_in_nav) > 0:
    print("\nFirst 20 Missing Codes:")
    print(sorted(list(missing_in_nav))[:20])

if len(extra_in_nav) > 0:
    print("\nFirst 20 Extra Codes:")
    print(sorted(list(extra_in_nav))[:20])

# -----------------------------
# Validation Status
# -----------------------------
if len(missing_in_nav) == 0:
    print("\n✅ All AMFI codes from Fund Master exist in NAV History.")
else:
    print("\n⚠️ Some AMFI codes are missing from NAV History.")

# -----------------------------
# Data Quality Summary
# -----------------------------
print("\n" + "=" * 70)
print("DATA QUALITY SUMMARY")
print("=" * 70)

print(f"Fund Master Rows : {len(fund_master):,}")
print(f"NAV History Rows : {len(nav_history):,}")

print(f"\nFund Master Missing Values :")
print(fund_master.isnull().sum().sum())

print(f"\nNAV History Missing Values :")
print(nav_history.isnull().sum().sum())

print(f"\nFund Master Duplicate Rows : {fund_master.duplicated().sum()}")
print(f"NAV History Duplicate Rows : {nav_history.duplicated().sum()}")

print("\nValidation Completed Successfully.")
print("=" * 70)
