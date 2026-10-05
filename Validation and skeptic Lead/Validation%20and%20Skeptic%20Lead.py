"""
Validation and Skeptic Lead
Combined Python checks extracted from the uploaded validation protocol.

Source: Combined Validation Protocol: Northstar / Suez Case
"""

raw_rows, clean_rows = len(raw), len(clean)
print("Raw:", raw_rows, "Clean:", clean_rows, "Removed:", raw_rows - clean_rows)
# Compare this to the sum of rows in the cleaning log. They must match.

key = ["date", "market", "channel", "sku"]
print("Duplicate keys after cleaning:", clean.duplicated(key).sum())  # should be 0
print("Unparseable dates:", clean["date"].isna().sum())
print("Date range:", clean["date"].min(), clean["date"].max())  # should end 2022-06-30
print("Negative units_sold:", (clean["units_sold"] < 0).sum())
print("Returns > units_sold:", (clean["returns_units"] > clean["units_sold"]).sum())

# Flag columns: check the mapping, not just the result
for col in flag_cols:
    print(raw[col].value_counts(dropna=False))
    print(clean[col].value_counts(dropna=False))


train_end = pd.Timestamp("2022-06-02")
test_start, test_end = pd.Timestamp("2022-06-03"), pd.Timestamp("2022-06-30")
assert train["date"].max() <= train_end
assert test["date"].min() == test_start and test["date"].max() == test_end
assert test["date"].unique() == 28
assert train["date"].max() < test["date"].min()  # no overlap
