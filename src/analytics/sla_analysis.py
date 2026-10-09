
import sys
sys.path.insert(0, ".")

from src.analytics.load_data import load_all

data = load_all()
orders = data["orders"]

print("\n" + "=" * 60)
print("MACROOPS AI — SLA PERFORMANCE ANALYSIS")
print("=" * 60)

# 1. Overall order status distribution
print("\n1. ORDER STATUS DISTRIBUTION")
print("-" * 40)

status_counts = orders["status"].value_counts(dropna=False)
status_pct = orders["status"].value_counts(
    normalize=True, dropna=False
) * 100

for status in status_counts.index:
    print(
        f"{status}: {status_counts[status]:,} "
        f"({status_pct[status]:.2f}%)"
    )

# 2. SLA breach rate across all orders
print("\n2. OVERALL SLA PERFORMANCE")
print("-" * 40)

total_orders = len(orders)
breached = orders["sla_breached"].sum()
breach_rate = breached / total_orders * 100

print(f"Total orders: {total_orders:,}")
print(f"Orders flagged as SLA breached: {breached:,}")
print(f"Overall SLA breach rate: {breach_rate:.2f}%")
print(f"Overall SLA-compliant rate: {100 - breach_rate:.2f}%")

# 3. Delivery delay distribution
print("\n3. DELIVERY DELAY SUMMARY")
print("-" * 40)

print(orders["delivery_delay_minutes"].describe().round(2).to_string())

# 4. SLA performance by order status
print("\n4. SLA BREACH RATE BY STATUS")
print("-" * 40)

status_sla = orders.groupby("status").agg(
    order_count=("order_id", "count"),
    breached_orders=("sla_breached", "sum"),
    average_recorded_delay=("delivery_delay_minutes", "mean")
)

status_sla["breach_rate_pct"] = (
    status_sla["breached_orders"] / status_sla["order_count"] * 100
)

print(status_sla.round(2).to_string())

# 5. Delay bands
print("\n5. DELAY BANDS")
print("-" * 40)

delay_bands = [
    ("0 minutes", orders["delivery_delay_minutes"] == 0),
    ("Above 0 to 5 minutes",
     (orders["delivery_delay_minutes"] > 0) &
     (orders["delivery_delay_minutes"] <= 5)),
    ("Above 5 to 10 minutes",
     (orders["delivery_delay_minutes"] > 5) &
     (orders["delivery_delay_minutes"] <= 10)),
    ("Above 10 to 15 minutes",
     (orders["delivery_delay_minutes"] > 10) &
     (orders["delivery_delay_minutes"] <= 15)),
    ("Above 15 minutes", orders["delivery_delay_minutes"] > 15),
]

for label, condition in delay_bands:
    count = condition.sum()
    print(f"{label}: {count:,} ({count / total_orders * 100:.2f}%)")

print("\nSLA analysis complete.")
