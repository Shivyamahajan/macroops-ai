import sys
sys.path.insert(0, ".")

from src.analytics.load_data import load_all

data = load_all()
orders = data["orders"].copy()

print("\n" + "=" * 65)
print("MACROOPS AI — STORE-LEVEL SLA ANALYSIS")
print("=" * 65)

# Calculate performance for each store
store_sla = orders.groupby("store_id").agg(
    total_orders=("order_id", "count"),
    late_orders=(
        "status",
        lambda s: (s == "Delivered_Late").sum()
    ),
    on_time_orders=(
        "status",
        lambda s: (s == "Delivered_On_Time").sum()
    ),
    average_delay=("delivery_delay_minutes", "mean")
)

store_sla["late_delivery_rate_pct"] = (
    store_sla["late_orders"]
    / (store_sla["late_orders"] + store_sla["on_time_orders"])
    * 100
)

store_sla = store_sla.sort_values(
    "late_delivery_rate_pct",
    ascending=False
)

print("\nTOP 10 STORES BY LATE-DELIVERY RATE")
print("-" * 65)
print(store_sla.head(10).round(2).to_string())

print("\nBOTTOM 10 STORES BY LATE-DELIVERY RATE")
print("-" * 65)
print(store_sla.tail(10).round(2).to_string())

print("\nOVERALL STORE SUMMARY")
print("-" * 65)
print(f"Stores analysed: {len(store_sla):,}")
print(f"Average store late-delivery rate: "
      f"{store_sla['late_delivery_rate_pct'].mean():.2f}%")
print(f"Highest store late-delivery rate: "
      f"{store_sla['late_delivery_rate_pct'].max():.2f}%")
print(f"Lowest store late-delivery rate: "
      f"{store_sla['late_delivery_rate_pct'].min():.2f}%")

print("\nStore-level SLA analysis complete.")
