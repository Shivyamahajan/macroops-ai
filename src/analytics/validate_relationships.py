
import sys
sys.path.insert(0, ".")

from src.analytics.load_data import load_all

data = load_all()

orders = data["orders"]
picking = data["picking"]
delivery = data["delivery"]
inventory = data["inventory"]
workforce = data["workforce"]

print("\n" + "=" * 60)
print("RELATIONSHIP VALIDATION")
print("=" * 60)

# 1. Check uniqueness of identifiers
print("\n1. IDENTIFIER UNIQUENESS")
print("-" * 40)

print("Orders — unique order IDs:",
      orders["order_id"].nunique(), "/", len(orders))
print("Picking — unique order IDs:",
      picking["order_id"].nunique(), "/", len(picking))
print("Delivery — unique order IDs:",
      delivery["order_id"].nunique(), "/", len(delivery))

print("Inventory — unique store/SKU pairs:",
      inventory[["store_id", "sku_id"]].drop_duplicates().shape[0],
      "/", len(inventory))

print("Workforce — unique employee IDs:",
      workforce["employee_id"].nunique(), "/", len(workforce))

# 2. Check order-to-picking and order-to-delivery coverage
print("\n2. ORDER MATCH COVERAGE")
print("-" * 40)

order_ids = set(orders["order_id"])
picking_ids = set(picking["order_id"])
delivery_ids = set(delivery["order_id"])

matched_picking = order_ids & picking_ids
matched_delivery = order_ids & delivery_ids

print(f"Orders with picking records: {len(matched_picking):,} "
      f"/ {len(order_ids):,} "
      f"({len(matched_picking) / len(order_ids) * 100:.2f}%)")

print(f"Orders with delivery records: {len(matched_delivery):,} "
      f"/ {len(order_ids):,} "
      f"({len(matched_delivery) / len(order_ids) * 100:.2f}%)")

print(f"Picking IDs not found in orders: {len(picking_ids - order_ids):,}")
print(f"Delivery IDs not found in orders: {len(delivery_ids - order_ids):,}")

# 3. Check store relationships
print("\n3. STORE MATCH COVERAGE")
print("-" * 40)

order_stores = set(orders["store_id"])
inventory_stores = set(inventory["store_id"])
workforce_stores = set(workforce["store_id"])

print(f"Order stores: {len(order_stores)}")
print(f"Inventory stores: {len(inventory_stores)}")
print(f"Workforce stores: {len(workforce_stores)}")

print("Order stores missing from inventory:",
      len(order_stores - inventory_stores))
print("Order stores missing from workforce:",
      len(order_stores - workforce_stores))

# 4. Check whether simple joins could multiply rows
print("\n4. JOIN CARDINALITY CHECK")
print("-" * 40)

for name, df in [("picking", picking), ("delivery", delivery)]:
    duplicate_keys = df["order_id"].duplicated().sum()
    print(f"{name.title()} rows with repeated order IDs after first occurrence: "
          f"{duplicate_keys:,}")

print("\nValidation complete. Review these results before merging datasets.")


print("\n5. WORKFORCE REPEATED-ID INVESTIGATION")
print("-" * 40)

print("Total workforce rows:", len(workforce))
print("Unique employees:", workforce["employee_id"].nunique())
print("Rows beyond the first occurrence of each employee:",
      workforce["employee_id"].duplicated().sum())

print("\nMost frequent employee IDs:")
print(workforce["employee_id"].value_counts().head(10).to_string())

print("\nExample records for one repeated employee:")
repeated_ids = workforce.loc[
    workforce["employee_id"].duplicated(keep=False),
    "employee_id"
]

if not repeated_ids.empty:
    example_id = repeated_ids.iloc[0]
    print(workforce[workforce["employee_id"] == example_id].to_string(index=False))
else:
    print("No repeated employee IDs found.")


print("\n6. WORKFORCE RECORD CONSISTENCY")
print("-" * 40)

for column in ["role", "store_id", "shift"]:
    counts = workforce.groupby("employee_id")[column].nunique()
    inconsistent = counts[counts > 1]

    print(
        f"Employees linked to multiple {column} values: "
        f"{len(inconsistent):,} / {workforce['employee_id'].nunique():,}"
    )

print("\nExample employee IDs with multiple roles:")
role_counts = workforce.groupby("employee_id")["role"].nunique()
multiple_roles = role_counts[role_counts > 1].index

if len(multiple_roles) > 0:
    print(
        workforce[workforce["employee_id"].isin(multiple_roles[:3])]
        .sort_values("employee_id")
        .to_string(index=False)
    )
else:
    print("No employees linked to multiple roles.")

print("\n7. PICKING-TO-DELIVERY COVERAGE")
print("-" * 40)

picking_ids = set(picking["order_id"])
delivery_ids = set(delivery["order_id"])

both_ids = picking_ids & delivery_ids
picking_only = picking_ids - delivery_ids
delivery_only = delivery_ids - picking_ids

print(f"Orders with both records: {len(both_ids):,}")
print(f"Orders with picking only: {len(picking_only):,}")
print(f"Orders with delivery only: {len(delivery_only):,}")

if len(picking_ids) > 0:
    print(
        f"Picking records also found in delivery: "
        f"{len(both_ids) / len(picking_ids) * 100:.2f}%"
    )

print("\nCheck complete.")

