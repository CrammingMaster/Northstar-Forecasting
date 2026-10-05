import pandas as pd

FILE = "northstar_event_impact_ready.csv"

df = pd.read_csv(FILE)

# ---------------------------------------------------------
# LOAD AND PREPARE DATA
# ---------------------------------------------------------

df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("=" * 70)
print("NORTHSTAR EVENT IMPACT METRICS")
print("=" * 70)

# ---------------------------------------------------------
# DEFINE PERIOD ORDER
# ---------------------------------------------------------

period_order = [
    "Pre-event",
    "Blockage",
    "Early recovery",
    "Later recovery"
]

df = df[df["event_period"].isin(period_order)].copy()

df["event_period"] = pd.Categorical(
    df["event_period"],
    categories=period_order,
    ordered=True
)

# ---------------------------------------------------------
# BASIC ROUTE CHECK
# ---------------------------------------------------------

print("\n[1] ROUTE EXPOSURE GROUPS")
print(df["route_exposure"].value_counts())

# ---------------------------------------------------------
# EVENT PERIOD SUMMARY
# ---------------------------------------------------------

print("\n[2] EVENT PERIOD SUMMARY")

summary = (
    df.groupby(
        ["event_period", "route_exposure"],
        observed=True
    )
    .agg(
        records=("date", "size"),
        units_sold=("units_sold", "sum"),
        avg_units_sold=("units_sold", "mean"),
        cancelled_units=("cancelled_units", "sum"),
        avg_cancelled_units=("cancelled_units", "mean"),
        stockout_rate=("stockout_flag", "mean"),
        avg_supplier_lead_days=("supplier_lead_days", "mean"),
        avg_transit_delay_days=("transit_delay_days", "mean"),
    )
    .reset_index()
)

summary["stockout_rate_pct"] = summary["stockout_rate"] * 100

print(summary.to_string(index=False))

# ---------------------------------------------------------
# GROSS MARGIN PROXY
# ---------------------------------------------------------

print("\n[3] GROSS-MARGIN PROXY")

df["fulfilled_units"] = df["units_sold"] - df["returns_units"]

df["gross_margin_proxy"] = (
    (df["unit_price_eur"] - df["unit_cost_eur"])
    * df["fulfilled_units"]
)

margin_summary = (
    df.groupby(
        ["event_period", "route_exposure"],
        observed=True
    )
    .agg(
        gross_margin_proxy=("gross_margin_proxy", "sum"),
        avg_gross_margin_proxy=("gross_margin_proxy", "mean")
    )
    .reset_index()
)

print(margin_summary.to_string(index=False))

# ---------------------------------------------------------
# COMBINE SUMMARY TABLES
# ---------------------------------------------------------

final_summary = summary.merge(
    margin_summary,
    on=["event_period", "route_exposure"],
    how="left"
)

# ---------------------------------------------------------
# SAVE SUMMARY
# ---------------------------------------------------------

OUTPUT_FILE = "event_impact_summary.csv"

final_summary.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n[4] SAVED SUMMARY")
print(OUTPUT_FILE)

# ---------------------------------------------------------
# WEEKLY OPERATIONAL SIGNALS
# ---------------------------------------------------------

print("\n[5] WEEKLY OPERATIONAL SIGNALS")

df["week"] = df["date"].dt.to_period("W").dt.start_time

weekly = (
    df.groupby(
        ["week", "route_exposure"],
        observed=True
    )
    .agg(
        units_sold=("units_sold", "sum"),
        cancelled_units=("cancelled_units", "sum"),
        stockout_rate=("stockout_flag", "mean"),
        avg_supplier_lead_days=("supplier_lead_days", "mean"),
        avg_transit_delay_days=("transit_delay_days", "mean")
    )
    .reset_index()
)

weekly["stockout_rate_pct"] = weekly["stockout_rate"] * 100

weekly.to_csv(
    "weekly_operational_signals.csv",
    index=False
)

print("weekly_operational_signals.csv")

# ---------------------------------------------------------
# EVENT IMPACT CHANGE FROM PRE-EVENT
# ---------------------------------------------------------

print("\n[6] CHANGE RELATIVE TO PRE-EVENT")

pre = final_summary[
    final_summary["event_period"] == "Pre-event"
].copy()

pre = pre.set_index("route_exposure")

comparison = final_summary.copy()

comparison["pre_event_avg_units_sold"] = (
    comparison["route_exposure"]
    .map(pre["avg_units_sold"])
)

comparison["change_avg_units_sold_pct"] = (
    (
        comparison["avg_units_sold"]
        - comparison["pre_event_avg_units_sold"]
    )
    / comparison["pre_event_avg_units_sold"]
) * 100

comparison["pre_event_stockout_rate_pct"] = (
    comparison["route_exposure"]
    .map(pre["stockout_rate_pct"])
)

comparison["change_stockout_rate_points"] = (
    comparison["stockout_rate_pct"]
    - comparison["pre_event_stockout_rate_pct"]
)

print(
    comparison[
        [
            "event_period",
            "route_exposure",
            "avg_units_sold",
            "change_avg_units_sold_pct",
            "stockout_rate_pct",
            "change_stockout_rate_points"
        ]
    ].to_string(index=False)
)

comparison.to_csv(
    "event_impact_comparison.csv",
    index=False
)

print("\n[7] SAVED COMPARISON")
print("event_impact_comparison.csv")

print("\n" + "=" * 70)
print("EVENT IMPACT METRICS COMPLETE")
print("=" * 70)