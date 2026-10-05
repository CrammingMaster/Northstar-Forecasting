import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. Load cleaned data
# ------------------------------------------------------------
df = pd.read_csv("northstar_clean.csv", parse_dates=["date"])

print("Shape:", df.shape)
print("Date range:", df["date"].min(), "to", df["date"].max())
print("Missing values:\n", df.isnull().sum())

# ------------------------------------------------------------
# 2. Commercial metrics
# ------------------------------------------------------------
df["margin_proxy_eur"] = df["revenue_eur"] - (df["unit_cost_eur"] * df["units_sold"])

# Exposed vs Control groups
exposed = df[df["route_exposure"] == "Asia-Suez"]
control = df[df["route_exposure"].isin(["Regional-Europe", "Air-or-Other"])]

# Event windows
pre_event_start = pd.Timestamp("2021-03-01")
pre_event_end   = pd.Timestamp("2021-03-22")
event_start     = pd.Timestamp("2021-03-23")
event_end       = pd.Timestamp("2021-03-29")
extended_end    = pd.Timestamp("2021-05-15")

def window_stats(data, start, end, label):
    w = data[(data["date"] >= start) & (data["date"] <= end)]
    return {
        "Window": label,
        "Rows": len(w),
        "Units sold": w["units_sold"].sum(),
        "Revenue €": w["revenue_eur"].sum(),
        "Margin proxy €": w["margin_proxy_eur"].sum(),
        "Stockout rate": w["stockout_flag"].mean(),
        "Cancellations": w["cancelled_units"].sum(),
        "Returns": w["returns_units"].sum(),
        "Promo days": w["promo_flag"].sum(),
        "Holiday days": w["holiday_flag"].sum(),
    }

stats = []
for label, start, end in [
    ("Pre-event (1–22 Mar 2021)", pre_event_start, pre_event_end),
    ("Event (23–29 Mar 2021)", event_start, event_end),
    ("Extended (23 Mar – 15 May 2021)", event_start, extended_end),
]:
    stats.append(window_stats(exposed, start, end, "Exposed – " + label))
    stats.append(window_stats(control, start, end, "Control – " + label))

print(pd.DataFrame(stats).to_string(index=False))

# ------------------------------------------------------------
# 3. SKU-level event impact
# ------------------------------------------------------------
sku_stats = []
for sku in exposed["sku"].unique():
    s = exposed[exposed["sku"] == sku]
    pre = s[(s["date"] >= pre_event_start) & (s["date"] <= pre_event_end)]
    ev  = s[(s["date"] >= event_start) & (s["date"] <= event_end)]
    if len(pre) == 0 or len(ev) == 0:
        continue
    sku_stats.append({
        "SKU": sku,
        "Pre units/day": pre["units_sold"].mean(),
        "Event units/day": ev["units_sold"].mean(),
        "Pre stockout rate": pre["stockout_flag"].mean(),
        "Event stockout rate": ev["stockout_flag"].mean(),
        "Pre transit delay": pre["transit_delay_days"].mean(),
        "Event transit delay": ev["transit_delay_days"].mean(),
    })

print(pd.DataFrame(sku_stats).to_string(index=False))

# ------------------------------------------------------------
# 4. Sensitivity tests (required by brief)
# ------------------------------------------------------------
def sensitivity(data, label):
    # 4-week pre
    pre4_start = event_start - pd.Timedelta(weeks=4)
    pre4 = data[(data["date"] >= pre4_start) & (data["date"] < event_start)]
    ev  = data[(data["date"] >= event_start) & (data["date"] <= extended_end)]
    # 6-week recovery
    rec = data[(data["date"] > extended_end) & (data["date"] <= extended_end + pd.Timedelta(weeks=6))]
    return {
        "Scenario": label,
        "Pre units/day": pre4["units_sold"].mean(),
        "Event+recovery units/day": ev["units_sold"].mean(),
        "Stockout rate (event+recovery)": ev["stockout_flag"].mean(),
        "Cancellations (event+recovery)": ev["cancelled_units"].sum(),
    }

sens = []
sens.append(sensitivity(exposed, "Exposed – 4‑wk pre, 8‑wk event+recovery"))
sens.append(sensitivity(control, "Control – 4‑wk pre, 8‑wk event+recovery"))
print(pd.DataFrame(sens).to_string(index=False))

# ------------------------------------------------------------
# 5. Forecast holdout check (NS‑003, NS‑033, NS‑048)
# ------------------------------------------------------------
holdout_start = pd.Timestamp("2022-06-03")
holdout_end   = pd.Timestamp("2022-06-30")

for sku in ["NS-003", "NS-033", "NS-048"]:
    s = df[df["sku"] == sku]
    train = s[s["date"] < holdout_start]
    test  = s[(s["date"] >= holdout_start) & (s["date"] <= holdout_end)]
    print(f"\n{sku}")
    print("  Last train date:", train["date"].max())
    print("  Holdout days:", test["date"].nunique())
    print("  Actual holdout units:", test["units_sold"].sum())
    print("  Holdout mean units/day:", test["units_sold"].mean())
    print("  Holdout stockout days:", test["stockout_flag"].sum())
    print("  Holdout promo days:", test["promo_flag"].sum())
    print("  Holdout transit delay mean:", test["transit_delay_days"].mean())