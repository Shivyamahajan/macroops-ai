
import sys
sys.path.insert(0, ".")

from src.analytics.load_data import load_all

data = load_all()

orders = data["orders"]
picking = data["picking"]
delivery = data["delivery"]

print("\n" + "=" * 60)
print("OPERATIONAL TIMESTAMP VALIDATION")
print("=" * 60)

# 1. Orders: compare delivery timestamps with order timestamps
print("\n1. ORDERS")
print("-" * 40)

order_time_checks = {
    "Actual delivery before order": (
        orders["actual_delivery_time"] < orders["order_time"]
    ),
    "Promised time before order": (
        orders["promised_time"] < orders["order_time"]
    ),
}

for label, condition in order_time_checks.items():
    print(f"{label}: {condition.sum():,}")

# Compare calculated delivery delay with the recorded delay.
# Restrict this comparison to delivered orders with valid timestamps.
delivered = orders[
    orders["status"].isin(["Delivered_Late", "Delivered_On_Time"])
].copy()

calculated_delay = (
    (delivered["actual_delivery_time"] - delivered["promised_time"])
    .dt.total_seconds() / 60
).clip(lower=0)

delay_difference = (
    calculated_delay - delivered["delivery_delay_minutes"]
).abs()

print("\nDelivered orders checked:", len(delivered))
print(
    "Delay differences greater than 1 minute:",
    (delay_difference > 1).sum()
)
print(
    "Maximum absolute delay difference (minutes):",
    round(delay_difference.max(), 2)
)

# 2. Picking: compare timestamps with recorded duration
print("\n2. PICKING")
print("-" * 40)

calculated_pick = (
    (picking["pick_end"] - picking["pick_start"])
    .dt.total_seconds() / 60
)

pick_difference = (
    calculated_pick - picking["pick_duration_minutes"]
).abs()

print(
    "Pick end before pick start:",
    (picking["pick_end"] < picking["pick_start"]).sum()
)
print(
    "Duration differences greater than 1 minute:",
    (pick_difference > 1).sum()
)
print(
    "Maximum absolute duration difference (minutes):",
    round(pick_difference.max(), 2)
)

# 3. Delivery: check event order
print("\n3. DELIVERY")
print("-" * 40)

print(
    "Pickup before assignment:",
    (delivery["pickup_time"] < delivery["assignment_time"]).sum()
)
print(
    "Delivery before pickup:",
    (delivery["delivery_time"] < delivery["pickup_time"]).sum()
)

print("\nTimestamp validation complete.")
