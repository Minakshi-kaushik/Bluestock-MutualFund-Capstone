from pathlib import Path
import requests
import pandas as pd

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Raw data folder
RAW_DATA_PATH = BASE_DIR / "data" / "raw"

# Create folder if it doesn't exist
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

# AMFI Codes provided in project instructions
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

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        # Convert NAV history to DataFrame
        nav_df = pd.DataFrame(data["data"])

        # Save file
        output_file = RAW_DATA_PATH / f"{fund_name}_live_nav.csv"
        nav_df.to_csv(output_file, index=False)

        print(f"Saved: {output_file.name}")
        print(f"Records: {len(nav_df)}")

    except requests.exceptions.RequestException as e:
        print(f"Network Error for {fund_name}: {e}")

    except KeyError:
        print(f"Unexpected API response for {fund_name}")

    except Exception as e:
        print(f"Error processing {fund_name}: {e}")

print("\n" + "=" * 70)
print("LIVE NAV FETCH COMPLETED")
print("=" * 70)
