from pathlib import Path
import requests
import pandas as pd

# Folder to save fetched NAV files
RAW_DATA_PATH = Path("data/raw")

# AMFI codes provided in project instructions
FUNDS = {
    "HDFC_Top_100_Direct": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

print("=" * 70)
print("LIVE NAV DATA FETCH")
print("=" * 70)

for fund_name, amfi_code in FUNDS.items():
    try:
        print(f"\nFetching {fund_name} ({amfi_code})...")

        url = f"https://api.mfapi.in/mf/{amfi_code}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        json_data = response.json()

        # NAV history returned by API
        nav_df = pd.DataFrame(json_data["data"])

        output_file = RAW_DATA_PATH / f"{fund_name}_live_nav.csv"

        nav_df.to_csv(output_file, index=False)

        print(f"Saved -> {output_file}")
        print(f"Records fetched: {len(nav_df)}")

    except Exception as e:
        print(f"Error fetching {fund_name}: {e}")

print("\n" + "=" * 70)
print("LIVE NAV FETCH COMPLETED")
print("=" * 70)
