import pandas as pd

FILE = "northstar_daily_sku_market.csv"

# Load the raw dataset
df = pd.read_csv(FILE)

print("=" * 60)
print("NORTHSTAR DATASET PROFILE")
print("=" * 60)

# 1. Dataset size
print("\n[1] DATASET SIZE")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Column names
print("\n[2] COLUMNS")
for column in df.columns:
    print("-", column)

# 3. Data types
print("\n[3] DATA TYPES")   
print(df.dtypes)

# 4. Missing values
print("\n[4] MISSING VALUES")
missing = df.isna().sum()
print(missing[missing > 0])

# 5. Duplicate rows
print("\n[5] EXACT DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())

# 6. First five rows
print("\n[6] FIRST 5 ROWS")
print(df.head())

print("\n" + "=" * 60)
print("PROFILE COMPLETE")
print("=" * 60)