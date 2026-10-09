
import sys
import pandas as pd

sys.path.insert(0, ".")

from src.analytics.load_data import load_all
from src.analytics.create_master_dataset import build_master_dataset


THRESHOLDS = {
    "sla_breach_rate": {"good": 5, "warning": 15},
    "on_time_delivery_rate": {"good": 95, "warning": 85},
    "avg_delay_minutes": {"good": 5, "warning": 10},
    "avg_pick_duration": {"good": 10, "warning": 20},
    "avg_assignment_delay": {"good": 5, "warning": 12},
    "missing_item_order_rate": {"good": 3, "warning": 8},
    "inventory_accuracy": {"good": 95, "warning": 85},
    "stockout_rate": {"good": 2, "warning": 5},
    "high_variance_rate": {"good": 5, "warning": 10},
    "task_completion_rate": {"good": 90, "warning": 75},
    "cancellation_rate": {"good": 2, "warning": 5},
}


def get_status(value, metric, higher_is_better=False):
    if pd.isna(value):
        return "N/A"

    limits = THRESHOLDS[metric]
    good = limits["good"]
    warning = limits["warning"]

    if higher_is_better:
        if value >= good:
            return "Good"
        if value >= warning:
            return "Warning"
        return "Critical"

    if value <= good:
        return "Good"
    if value <= warning:
        return "Warning"
    return "Critical"


def make_kpi(value, metric, unit="%", higher_is_better=False, detail=""):
    return {
        "value": round(float(value), 2) if pd.notna(value) else None,
        "unit": unit,
        "status": get_status(value, metric, higher_is_better),
        "detail": detail,
    }


def calculate_all_kpis(data, master, store_id=None):
    orders = data["orders"].copy()
    inventory = data["inventory"].copy()
    workforce = data["workforce"].copy()

    # Normalize stockout values before calculating the rate.
    stockout_values = (
        inventory["stockout"].astype(str).str.strip().str.lower()
    )
    stockout_mapping = {
        "true": True, "false": False,
        "1": True, "0": False,
        "yes": True, "no": False,
        "y": True, "n": False,
    }
    inventory["stockout"] = stockout_values.map(stockout_mapping)

    if inventory["stockout"].isna().any():
        bad_values = stockout_values[inventory["stockout"].isna()].unique()
        raise ValueError(f"Unexpected stockout values: {bad_values}")

    # Apply one consistent store filter to each dataset.
    if store_id is not None:
        orders = orders[orders["store_id"] == store_id]
        master = master[master["store_id"] == store_id]
        inventory = inventory[inventory["store_id"] == store_id]
        workforce = workforce[workforce["store_id"] == store_id]

        if orders.empty:
            raise ValueError(f"No orders found for store {store_id}.")

    delivered = orders[
        orders["status"].isin(["Delivered_Late", "Delivered_On_Time"])
    ]
    late_delivered = delivered[
        delivered["status"] == "Delivered_Late"
    ]
    on_time_delivered = delivered[
        delivered["status"] == "Delivered_On_Time"
    ]

    total_orders = len(orders)
    delivered_count = len(delivered)

    breach_rate = (
        len(late_delivered) / delivered_count * 100
        if delivered_count else float("nan")
    )
    on_time_rate = (
        len(on_time_delivered) / delivered_count * 100
        if delivered_count else float("nan")
    )

    # Mean delay for delivered-late orders only.
    late_ids = set(late_delivered["order_id"])
    late_delays = master.loc[
        master["order_id"].isin(late_ids), "delivery_delay_minutes"
    ].dropna()
    avg_delay = (
        late_delays.mean() if not late_delays.empty else float("nan")
    )

    pick_durations = master["pick_duration_minutes"].dropna()
    assignment_delays = master["assignment_delay_minutes"].dropna()

    picking_records = master.dropna(subset=["items_missing"])
    missing_item_rate = (
        (picking_records["items_missing"] > 0).mean() * 100
        if not picking_records.empty else float("nan")
    )

    cancellation_rate = (
        (orders["status"] == "Cancelled").mean() * 100
        if total_orders else float("nan")
    )

    inventory_accuracy = inventory["inventory_accuracy_pct"].mean()
    stockout_rate = (
        inventory["stockout"].mean() * 100
        if not inventory.empty else float("nan")
    )
    high_variance_rate = (
        (inventory["stock_variance"].abs() > 10).mean() * 100
        if not inventory.empty else float("nan")
    )

    completed_tasks = workforce["tasks_completed"].sum()
    pending_tasks = workforce["tasks_pending"].sum()
    all_tasks = completed_tasks + pending_tasks
    task_completion_rate = (
        completed_tasks / all_tasks * 100
        if all_tasks else float("nan")
    )

    kpis = {
        "order_volume": {
            "value": int(total_orders),
            "unit": "orders",
            "status": "N/A",
            "detail": f"{total_orders:,} orders in this scope.",
        },
        "delivered_orders": {
            "value": int(delivered_count),
            "unit": "orders",
            "status": "N/A",
            "detail": "Delivered late plus delivered on time.",
        },
        "sla_breach_rate": make_kpi(
            breach_rate, "sla_breach_rate",
            detail=f"{len(late_delivered):,} late / {delivered_count:,} delivered orders.",
        ),
        "on_time_delivery_rate": make_kpi(
            on_time_rate, "on_time_delivery_rate", higher_is_better=True,
            detail=f"{len(on_time_delivered):,} on time / {delivered_count:,} delivered orders.",
        ),
        "avg_delay_minutes": make_kpi(
            avg_delay, "avg_delay_minutes", unit="minutes",
            detail=f"Late-delivery delay records: {len(late_delays):,}.",
        ),
        "avg_pick_duration": make_kpi(
            pick_durations.mean(), "avg_pick_duration", unit="minutes",
            detail=f"Picking records available: {len(pick_durations):,}.",
        ),
        "avg_assignment_delay": make_kpi(
            assignment_delays.mean(), "avg_assignment_delay", unit="minutes",
            detail=f"Delivery records available: {len(assignment_delays):,}.",
        ),
        "missing_item_order_rate": make_kpi(
            missing_item_rate, "missing_item_order_rate",
            detail=f"Picking records available: {len(picking_records):,}.",
        ),
        "inventory_accuracy": make_kpi(
            inventory_accuracy, "inventory_accuracy", higher_is_better=True,
            detail=f"Inventory records: {len(inventory):,}.",
        ),
        "stockout_rate": make_kpi(
            stockout_rate, "stockout_rate",
            detail=f"Inventory records: {len(inventory):,}.",
        ),
        "high_variance_rate": make_kpi(
            high_variance_rate, "high_variance_rate",
            detail="Inventory rows with absolute stock variance greater than 10.",
        ),
        "task_completion_rate": make_kpi(
            task_completion_rate, "task_completion_rate", higher_is_better=True,
            detail=f"{completed_tasks:,.0f} completed / {all_tasks:,.0f} total tasks.",
        ),
        "cancellation_rate": make_kpi(
            cancellation_rate, "cancellation_rate",
            detail=f"Cancelled orders / {total_orders:,} total orders.",
        ),
        "scope": {
            "value": store_id if store_id is not None else "All stores",
            "unit": "",
            "status": "N/A",
            "detail": "Synthetic data; KPI thresholds are example targets.",
        },
    }

    return kpis


def print_kpis(kpis):
    print("\nOPERATIONAL KPI REPORT")
    print("=" * 65)

    for name, result in kpis.items():
        value = result["value"]
        unit = result["unit"]

        if value is None:
            displayed = "N/A"
        elif unit == "%":
            displayed = f"{value:.2f}%"
        elif unit == "minutes":
            displayed = f"{value:.2f} minutes"
        elif unit == "orders":
            displayed = f"{value:,}"
        else:
            displayed = str(value)

        print(f"\n{name.replace('_', ' ').title()}: {displayed}")
        print(f"  Status: {result['status']}")
        print(f"  Detail: {result['detail']}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    data = load_all()
    master = build_master_dataset()

    selected_store = None  # Change to "ST044" to analyse one store.

    results = calculate_all_kpis(
        data=data,
        master=master,
        store_id=selected_store,
    )
    print_kpis(results)
