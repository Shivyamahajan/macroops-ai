
import sys
sys.path.insert(0, ".")

from src.analytics.load_data import load_all
from pathlib import Path

data = load_all()

orders = data["orders"]
picking = data["picking"]
delivery = data["delivery"]

print("\nBuilding operational master dataset...")

# Validate keys before merging
assert orders["order_id"].is_unique, "Duplicate order IDs found"
assert picking["order_id"].is_unique, "Duplicate picking order IDs found"
assert delivery["order_id"].is_unique, "Duplicate delivery order IDs found"

# Prefix non-key columns to avoid ambiguous column names
picking = picking.rename(
    columns={
        col: f"picking_{col}"
        for col in picking.columns
        if col != "order_id"
    }
)

delivery = delivery.rename(
    columns={
        col: f"delivery_{col}"
        for col in delivery.columns
        if col != "order_id"
    }
)

# Keep every order and attach available operational records
master = orders.merge(
    picking,
    on="order_id",
    how="left",
    validate="one_to_one"
)

master = master.merge(
    delivery,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# Verify that the joins did not multiply or drop orders
assert len(master) == len(orders), "Unexpected row-count change"
assert master["order_id"].is_unique, "Duplicate order IDs after merge"

# Save the result
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "master_operational.csv"
master.to_csv(output_path, index=False)

print("\nMaster dataset created successfully.")
print(f"Rows: {len(master):,}")
print(f"Columns: {len(master.columns)}")
print(f"Orders without picking data: {master['picking_picker_id'].isna().sum():,}")
print(f"Orders without delivery data: {master['delivery_rider_id'].isna().sum():,}")
print(f"Saved to: {output_path}")


print("\n" + "=" * 50)
print("MASTER DATASET VERIFICATION")
print("=" * 50)

# Reload the saved file
from src.analytics.load_data import load_master

verified = load_master()

print("\nShape:", verified.shape)
print("Unique order IDs:", verified["order_id"].nunique())
print("Duplicate order IDs:", verified["order_id"].duplicated().sum())
print("Total missing values:", verified.isna().sum().sum())

print("\nFirst five rows:")
print(verified.head().to_string(index=False))

print("\nMissing values in operational columns:")
for column in ["picking_picker_id", "delivery_rider_id"]:
    print(f"{column}: {verified[column].isna().sum():,}")
