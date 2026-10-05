import pandas as pd

FILE = "northstar_daily_sku_market.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("NORTHSTAR DATA QUALITY INSPECTION")
print("=" * 70)


# 1. DATE VALUES
print("\n[1] DATE INSPECTION")
print("Sample date values:")
print(df["date"].head(20).to_string(index=False))

print("\nNumber of unique date values:", df["date"].nunique())


# 2. MARKET VALUES
print("\n[2] MARKET VALUES")
print(df["market"].value_counts(dropna=False))


# 3. CHANNEL VALUES
print("\n[3] CHANNEL VALUES")
print(df["channel"].value_counts(dropna=False))


# 4. PROMO FLAG VALUES
print("\n[4] PROMO FLAG VALUES")
print(df["promo_flag"].value_counts(dropna=False))


# 5. TRANSIT DELAY VALUES
print("\n[5] TRANSIT DELAY VALUES")
print(df["transit_delay_days"].value_counts(dropna=False).head(30))


# 6. NUMERIC SUMMARY
print("\n[6] NUMERIC SUMMARY")
print(df.describe(include="all").transpose())


# 7. BUSINESS KEY DUPLICATES
print("\n[7] BUSINESS KEY DUPLICATES")

key_columns = [
    "date",
    "market",
    "channel",
    "sku"
]

duplicate_keys = df.duplicated(
    subset=key_columns,
    keep=False
)

print("Rows involved in duplicate business keys:",
      duplicate_keys.sum())


# 8. NEGATIVE VALUES
print("\n[8] NEGATIVE VALUES")

numeric_columns = [
    "unit_price_eur",
    "unit_cost_eur",
    "planned_marketing_spend_eur",
    "opening_inventory_units",
    "inbound_received_units",
    "supplier_lead_days",
    "units_sold",
    "returns_units",
    "cancelled_units",
    "revenue_eur"
]

for column in numeric_columns:
    negative_count = (df[column] < 0).sum()
    print(f"{column}: {negative_count}")


print("\n" + "=" * 70)
print("QUALITY INSPECTION COMPLETE")
print("=" * 70)
# 9. PROBLEMATIC UNIT PRICES
print("\n[9] NEGATIVE UNIT PRICES")
print(
    df[df["unit_price_eur"] < 0][
        ["date", "market", "channel", "sku", "unit_price_eur"]
    ].to_string(index=False)
)


# 10. NEGATIVE UNITS SOLD
print("\n[10] NEGATIVE UNITS SOLD")
print(
    df[df["units_sold"] < 0][
        ["date", "market", "channel", "sku", "units_sold"]
    ].to_string(index=False)
)


# 11. INVALID TRANSIT DELAYS
print("\n[11] INVALID TRANSIT DELAYS")
print(
    df[df["transit_delay_days"].isin(["unknown", "-1"])][
        ["date", "market", "channel", "sku", "transit_delay_days"]
    ].to_string(index=False)
)


# 12. EXACT DUPLICATE ROWS
print("\n[12] EXACT DUPLICATE ROWS")
exact_duplicates = df[df.duplicated(keep=False)]

print(exact_duplicates.head(20).to_string(index=False))


# 13. BUSINESS KEY DUPLICATES
print("\n[13] BUSINESS KEY DUPLICATES")

key_columns = [
    "date",
    "market",
    "channel",
    "sku"
]

business_duplicates = df[
    df.duplicated(subset=key_columns, keep=False)
].sort_values(key_columns)

print(
    business_duplicates[
        key_columns + ["units_sold", "unit_price_eur", "revenue_eur"]
    ].head(50).to_string(index=False)
)
# 14. DATE PARSING INSPECTION
print("\n[14] DATE PARSING INSPECTION")

parsed_dates = pd.to_datetime(
    df["date"],
    errors="coerce"
)

print("Successfully parsed dates:", parsed_dates.notna().sum())
print("Unparseable dates:", parsed_dates.isna().sum())

print("\nUnparseable date values:")
print(
    df.loc[parsed_dates.isna(), "date"]
    .value_counts()
    .head(50)
)

print("\nParsed date range:")
print("Minimum:", parsed_dates.min())
print("Maximum:", parsed_dates.max())
# 15. MULTI-FORMAT DATE PARSING TEST
print("\n[15] MULTI-FORMAT DATE PARSING TEST")

raw_dates = df["date"].astype(str).str.strip()

# First attempt: standard month/day/year
parsed_dates = pd.to_datetime(
    raw_dates,
    format="%m/%d/%Y",
    errors="coerce"
)

# Second attempt: dates such as 11-Mar-21
mask = parsed_dates.isna()

parsed_dates.loc[mask] = pd.to_datetime(
    raw_dates.loc[mask],
    format="%d-%b-%y",
    errors="coerce"
)

print("Successfully parsed:", parsed_dates.notna().sum())
print("Still unparseable:", parsed_dates.isna().sum())

print("\nStill-unparseable values:")
print(
    raw_dates.loc[parsed_dates.isna()]
    .value_counts()
    .head(30)
)

print("\nFinal date range:")
print("Minimum:", parsed_dates.min())
print("Maximum:", parsed_dates.max())