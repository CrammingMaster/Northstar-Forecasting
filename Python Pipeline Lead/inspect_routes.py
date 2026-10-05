import pandas as pd

FILE = "northstar_clean.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("NORTHSTAR ROUTE EXPOSURE INSPECTION")
print("=" * 70)

print("\n[1] ROUTE EXPOSURE VALUES")
print(df["route_exposure"].value_counts(dropna=False))

print("\n[2] ROUTE EXPOSURE BY SKU CATEGORY")
print(
    pd.crosstab(
        df["route_exposure"],
        df["category"]
    )
)

print("\n[3] SUPPLIER REGION")
print(df["supplier_region"].value_counts(dropna=False))

print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)