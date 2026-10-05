import pandas as pd

FILE = "northstar_clean.csv"

df = pd.read_csv(FILE)

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("=" * 70)
print("NORTHSTAR EVENT IMPACT ANALYSIS")
print("=" * 70)


# ============================================================
# 1. DEFINE EVENT WINDOWS
# ============================================================

PRE_START = pd.Timestamp("2021-01-26")
PRE_END = pd.Timestamp("2021-03-22")

EVENT_START = pd.Timestamp("2021-03-23")
EVENT_END = pd.Timestamp("2021-03-29")

EARLY_RECOVERY_START = pd.Timestamp("2021-03-30")
EARLY_RECOVERY_END = pd.Timestamp("2021-04-12")

LATER_RECOVERY_START = pd.Timestamp("2021-04-13")
LATER_RECOVERY_END = pd.Timestamp("2021-05-24")


# ============================================================
# 2. DISPLAY WINDOWS
# ============================================================

print("\n[1] ANALYSIS WINDOWS")

print(
    "Pre-event:",
    PRE_START.date(),
    "to",
    PRE_END.date()
)

print(
    "Blockage:",
    EVENT_START.date(),
    "to",
    EVENT_END.date()
)

print(
    "Early recovery:",
    EARLY_RECOVERY_START.date(),
    "to",
    EARLY_RECOVERY_END.date()
)

print(
    "Later recovery:",
    LATER_RECOVERY_START.date(),
    "to",
    LATER_RECOVERY_END.date()
)


# ============================================================
# 3. ASSIGN PERIOD LABEL
# ============================================================

df["event_period"] = "Outside"

df.loc[
    (df["date"] >= PRE_START) &
    (df["date"] <= PRE_END),
    "event_period"
] = "Pre-event"

df.loc[
    (df["date"] >= EVENT_START) &
    (df["date"] <= EVENT_END),
    "event_period"
] = "Blockage"

df.loc[
    (df["date"] >= EARLY_RECOVERY_START) &
    (df["date"] <= EARLY_RECOVERY_END),
    "event_period"
] = "Early recovery"

df.loc[
    (df["date"] >= LATER_RECOVERY_START) &
    (df["date"] <= LATER_RECOVERY_END),
    "event_period"
] = "Later recovery"


# ============================================================
# 4. CHECK ROW COUNTS
# ============================================================

print("\n[2] ROW COUNTS BY PERIOD")

period_counts = df["event_period"].value_counts()

print(period_counts)


# ============================================================
# 5. CHECK DATE COVERAGE
# ============================================================

print("\n[3] ACTUAL DATE COVERAGE")

for period in [
    "Pre-event",
    "Blockage",
    "Early recovery",
    "Later recovery"
]:

    period_dates = df.loc[
        df["event_period"] == period,
        "date"
    ].dropna()

    print(
        f"{period}:",
        period_dates.min().date(),
        "to",
        period_dates.max().date()
    )


# ============================================================
# 6. SAVE EVENT IMPACT DATA
# ============================================================

OUTPUT_FILE = "northstar_event_impact_ready.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("EVENT IMPACT SETUP COMPLETE")
print("=" * 70)

print("Saved:", OUTPUT_FILE)