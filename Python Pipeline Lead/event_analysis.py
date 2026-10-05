import pandas as pd

FILE = "northstar_clean.csv"

df = pd.read_csv(FILE)

# Convert date back to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("=" * 70)
print("NORTHSTAR EVENT WINDOW ANALYSIS")
print("=" * 70)

# ============================================================
# 1. DEFINE EVENT WINDOW
# ============================================================

EVENT_START = pd.Timestamp("2021-03-23")
EVENT_END = pd.Timestamp("2021-03-29")

print("\n[1] EVENT WINDOW")
print("Event start:", EVENT_START.date())
print("Event end:", EVENT_END.date())


# ============================================================
# 2. LABEL EACH RECORD
# ============================================================

df["event_period"] = "Other"

df.loc[
    (df["date"] >= EVENT_START) &
    (df["date"] <= EVENT_END),
    "event_period"
] = "Event"


# ============================================================
# 3. CHECK EVENT RECORDS
# ============================================================

print("\n[2] EVENT RECORDS")

print(
    df["event_period"].value_counts()
)


# ============================================================
# 4. SHOW EVENT-DATE COVERAGE
# ============================================================

print("\n[3] EVENT DATE COVERAGE")

event_dates = df.loc[
    df["event_period"] == "Event",
    "date"
].dropna().drop_duplicates().sort_values()

print(event_dates.to_string(index=False))


# ============================================================
# 5. SAVE EVENT-READY DATA
# ============================================================

OUTPUT_FILE = "northstar_event_ready.csv"

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("EVENT PREPARATION COMPLETE")
print("=" * 70)

print("Saved:", OUTPUT_FILE)