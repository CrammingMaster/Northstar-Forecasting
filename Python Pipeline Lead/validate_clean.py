import pandas as pd

FILE = "northstar_clean.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("NORTHSTAR CLEAN DATA VALIDATION")
print("=" * 70)

# ============================================================
# 1. DATASET SIZE
# ============================================================

print("\n[1] DATASET SIZE")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 2. DATE VALIDATION
# ============================================================

print("\n[2] DATE VALIDATION")

df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("Valid dates:", df["date"].notna().sum())
print("Missing dates:", df["date"].isna().sum())

print("Minimum date:", df["date"].min())
print("Maximum date:", df["date"].max())


# ============================================================
# 3. MARKET VALIDATION
# ============================================================

print("\n[3] MARKET VALIDATION")

print(df["market"].value_counts(dropna=False))


# ============================================================
# 4. CHANNEL VALIDATION
# ============================================================

print("\n[4] CHANNEL VALIDATION")

print(df["channel"].value_counts(dropna=False))


# ============================================================
# 5. PROMO FLAG VALIDATION
# ============================================================

print("\n[5] PROMO FLAG VALIDATION")

print(df["promo_flag"].value_counts(dropna=False))


# ============================================================
# 6. NEGATIVE VALUE VALIDATION
# ============================================================

print("\n[6] NEGATIVE VALUE VALIDATION")

print("Negative unit prices:",
      (df["unit_price_eur"] < 0).sum())

print("Negative units sold:",
      (df["units_sold"] < 0).sum())

print("Negative transit delays:",
      (df["transit_delay_days"] < 0).sum())


# ============================================================
# 7. EXACT DUPLICATE VALIDATION
# ============================================================

print("\n[7] EXACT DUPLICATE VALIDATION")

print("Exact duplicate rows:", df.duplicated().sum())


# ============================================================
# 8. BUSINESS KEY VALIDATION
# ============================================================

print("\n[8] BUSINESS KEY VALIDATION")

key_columns = [
    "date",
    "market",
    "channel",
    "sku"
]

valid_dates = df["date"].notna()

duplicate_keys = df.loc[
    valid_dates
].duplicated(
    subset=key_columns,
    keep=False
)

print(
    "Duplicate business-key rows:",
    duplicate_keys.sum()
)


# ============================================================
# 9. MISSING VALUES
# ============================================================

print("\n[9] REMAINING MISSING VALUES")

missing = df.isna().sum()

print(
    missing[missing > 0]
)


# ============================================================
# 10. FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)