
import os
import sys
import pandas as pd

sys.path.insert(0, ".")

from src.analytics.load_data import load_all


OUTPUT_PATH = "data/processed/master_operational_all_tables.csv"


def aggregate_inventory_to_store(inventory):
    """Create one inventory summary row per store."""
    inventory = inventory.copy()

    inventory["abs_stock_variance"] = inventory["stock_variance"].abs()
    inventory["is_high_variance"] = (
        inventory["abs_stock_variance"] > 10
    )
    inventory["is_negative_variance"] = (
        inventory["stock_variance"] < 0
    )

    summary = inventory.groupby("store_id").agg(
        avg_inventory_accuracy=("inventory_accuracy_pct", "mean"),
        min_inventory_accuracy=("inventory_accuracy_pct", "min"),
        stockout_count=("stockout", "sum"),
        high_variance_count=("is_high_variance", "sum"),
        avg_abs_stock_variance=("abs_stock_variance", "mean"),
        negative_variance_items=("is_negative_variance", "sum"),
        total_skus=("sku_id", "nunique"),
    ).reset_index()

    summary["has_low_accuracy_store"] = (
        summary["avg_inventory_accuracy"] < 85
    )

    return summary


def aggregate_workforce_to_store(workforce):
    """Create one workforce summary row per store."""
    workforce = workforce.copy()

    summary = workforce.groupby("store_id").agg(
        total_unique_employees=("employee_id", "nunique"),
        avg_tasks_pending=("tasks_pending", "mean"),
        max_tasks_pending=("tasks_pending", "max"),
        overloaded_workforce_records=(
            "tasks_pending",
            lambda values: (values > 10).sum()
        ),
        total_tasks_completed=("tasks_completed", "sum"),
        total_tasks_pending=("tasks_pending", "sum"),
    ).reset_index()

    # Count unique employees with the Picker role, rather than rows.
    picker_counts = (
        workforce.loc[workforce["role"] == "Picker"]
        .groupby("store_id")["employee_id"]
        .nunique()
        .rename("unique_pickers")
        .reset_index()
    )

    summary = summary.merge(
        picker_counts,
        on="store_id",
        how="left",
        validate="one_to_one",
    )

    summary["unique_pickers"] = (
        summary["unique_pickers"].fillna(0).astype(int)
    )

    total_tasks = (
        summary["total_tasks_completed"]
        + summary["total_tasks_pending"]
    )

    summary["task_completion_rate_pct"] = (
        summary["total_tasks_completed"]
        .div(total_tasks.where(total_tasks != 0))
        .mul(100)
    )

    summary["is_store_overloaded"] = (
        summary["avg_tasks_pending"] > 8
    )

    return summary


def build_master_dataset(data=None):
    """Join all five datasets while preserving one row per order."""
    if data is None:
        data = load_all()

    orders = data["orders"].copy()
    picking = data["picking"].copy()
    delivery = data["delivery"].copy()
    inventory = data["inventory"].copy()
    workforce = data["workforce"].copy()

    # Parse timestamps before calculating time-based features.
    timestamp_columns = {
        "orders": [
            "order_time",
            "promised_time",
            "actual_delivery_time",
        ],
        "picking": ["pick_start", "pick_end"],
        "delivery": [
            "assignment_time",
            "pickup_time",
            "delivery_time",
        ],
    }

    for column in timestamp_columns["orders"]:
        orders[column] = pd.to_datetime(
            orders[column], errors="coerce"
        )

    for column in timestamp_columns["picking"]:
        picking[column] = pd.to_datetime(
            picking[column], errors="coerce"
        )

    for column in timestamp_columns["delivery"]:
        delivery[column] = pd.to_datetime(
            delivery[column], errors="coerce"
        )

    # Order-level time features.
    orders["order_hour"] = orders["order_time"].dt.hour
    orders["order_day_of_week"] = orders["order_time"].dt.dayofweek
    orders["order_day_name"] = orders["order_time"].dt.day_name()

    peak_hours = [12, 13, 18, 19, 20, 21]
    orders["is_peak_hour"] = orders["order_hour"].isin(peak_hours)

    orders["sla_window_minutes"] = (
        orders["promised_time"] - orders["order_time"]
    ).dt.total_seconds() / 60

    # Prepare picking features.
    picking_features = picking[
        [
            "order_id",
            "picker_id",
            "items_picked",
            "items_missing",
            "pick_duration_minutes",
        ]
    ].copy()

    picking_features["has_missing_items"] = (
        picking_features["items_missing"] > 0
    )
    picking_features["is_slow_pick"] = (
        picking_features["pick_duration_minutes"] > 20
    )

    # Prepare delivery features.
    delivery_features = delivery[
        [
            "order_id",
            "rider_id",
            "distance_km",
            "assignment_delay_minutes",
            "assignment_time",
            "pickup_time",
            "delivery_time",
        ]
    ].copy()

    delivery_features["pickup_duration_minutes"] = (
        delivery_features["pickup_time"]
        - delivery_features["assignment_time"]
    ).dt.total_seconds() / 60

    delivery_features["delivery_duration_minutes"] = (
        delivery_features["delivery_time"]
        - delivery_features["pickup_time"]
    ).dt.total_seconds() / 60

    delivery_features["is_high_assignment_delay"] = (
        delivery_features["assignment_delay_minutes"] > 15
    )

    # Merge order-level data. The validation checks prevent row multiplication.
    master = orders.merge(
        picking_features,
        on="order_id",
        how="left",
        validate="one_to_one",
    )

    master = master.merge(
        delivery_features,
        on="order_id",
        how="left",
        validate="one_to_one",
        suffixes=("", "_delivery"),
    )

    # Aggregate store-level data before joining it to orders.
    inventory_summary = aggregate_inventory_to_store(inventory)
    workforce_summary = aggregate_workforce_to_store(workforce)

    master = master.merge(
        inventory_summary,
        on="store_id",
        how="left",
        validate="many_to_one",
    )

    master = master.merge(
        workforce_summary,
        on="store_id",
        how="left",
        validate="many_to_one",
    )

    # Derived order features.
    master["total_fulfillment_minutes"] = (
        master["actual_delivery_time"] - master["order_time"]
    ).dt.total_seconds() / 60

    master["order_complexity"] = pd.cut(
        master["item_count"],
        bins=[-float("inf"), 3, 7, float("inf")],
        labels=["Low", "Medium", "High"],
    )

    # Final validation.
    if master["order_id"].duplicated().any():
        raise ValueError(
            "Duplicate order_id values found in the master dataset."
        )

    if len(master) != len(orders):
        raise ValueError(
            "Master dataset row count differs from the orders table."
        )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    master.to_csv(OUTPUT_PATH, index=False)

    print("\nMASTER DATASET CREATED")
    print("-" * 50)
    print(f"Output file: {OUTPUT_PATH}")
    print(f"Rows: {len(master):,}")
    print(f"Columns: {len(master.columns)}")
    print(f"Unique orders: {master['order_id'].nunique():,}")
    print(f"Duplicate order IDs: {master['order_id'].duplicated().sum():,}")
    print(f"Missing cells: {master.isna().sum().sum():,}")
    print("\nMissing values in key joined features:")
    for column in [
        "pick_duration_minutes",
        "assignment_delay_minutes",
        "avg_inventory_accuracy",
        "avg_tasks_pending",
    ]:
        print(f"  {column}: {master[column].isna().sum():,}")

    print("\nNote: inventory and workforce columns are store-level summaries.")
    print("The source data is synthetic, not live business data.")

    return master


if __name__ == "__main__":
    build_master_dataset()
