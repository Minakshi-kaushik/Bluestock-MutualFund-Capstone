from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw")

print("=" * 70)

print("BLUESTOCK MUTUAL FUND CAPSTONE - DATA INGESTION")
print("=" * 70)


csv_files = sorted(RAW_DATA_PATH.glob("*.csv"))


for file in csv_files:
    print("\n" + "=" * 70)
    print(f"Dataset: {file.name}")
    print("=" * 70)

    try:
        df = pd.read_csv(file)

        print(f"\nShape: {df.shape}")

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())
        print("\nMemory Usage (MB):")
        print(round(df.memory_usage(deep=True).sum() / 1024**2, 2))

        print("\nFirst 5 Rows:")
        print(df.head())

    except Exception as e:
        print(f"Error reading {file.name}: {e}")

print("\n")
print("=" * 70)
print("DATA INGESTION cOMPLETED")
print("=" * 70)
