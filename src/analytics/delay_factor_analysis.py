import sys
sys.path.insert(0, ".")

from src.analytics.load_data import load_all
import pandas as pd

data = load_all()
master = data["orders"].merge(
    data["picking"],
    on="order_id",
    how="left",
    validate="one_to_one"
)

master = master.merge(
    data["delivery"],
    on="order_id",
    how="left",
    validate="one_to_one",
    suffixes=("_picking", "_delivery")
)

print("\n" + "=" * 65)
print("MACROOPS AI — DELAY FACTOR ANALYSIS")
print("=" * 65)

# Analyse only orders with a recorded delivered status
delivered = master[
    master["status"].isin(["Delivered_Late", "Delivered_On_Time"])
].copy()

delivered["is_late"] = (
    delivered["status"] == "Delivered_Late"
).astype(int)

print(f"\nDelivered orders analysed: {len(delivered):,}")

# Compare operational metrics for late vs on-time deliveries
metrics = [
    ("pick_duration_minutes", "Picking duration (minutes)"),
    ("assignment_delay_minutes", "Rider assignment delay (minutes)"),
    ("distance_km", "Delivery distance (km)"),
    ("item_count", "Items per order"),
]

print("\nAVERAGE METRICS BY DELIVERY STATUS")
print("-" * 65)

for column, label in metrics:
    if column not in delivered.columns:
        print(f"\nSkipping {label}: column not found.")
        continue

    summary = delivered.groupby("status")[column].mean()

    print(f"\n{label}")
    for status, value in summary.items():
        print(f"  {status}: {value:.2f}")

# Compare available operational data coverage
print("\nOPERATIONAL DATA COVERAGE")
print("-" * 65)

for column, label in metrics:
    if column in delivered.columns:
        available = delivered[column].notna().sum()
        print(
            f"{label}: {available:,}/{len(delivered):,} "
            f"({available / len(delivered) * 100:.2f}%)"
        )

print("\nDelay factor analysis complete.")
