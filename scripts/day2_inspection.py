# scripts/day2_inspection.py

import pandas as pd
import os

DATA_PATH = "data/raw"

for file in os.listdir(DATA_PATH):
    if file.endswith(".csv"):
        print("\n" + "=" * 80)
        print(f"FILE: {file}")
        print("=" * 80)

        df = pd.read_csv(os.path.join(DATA_PATH, file))

        print("\nShape:")
        print(df.shape)

        print("\nColumns:")
        print(df.columns.tolist())

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        print("\nFirst 5 Rows:")
        print(df.head())
