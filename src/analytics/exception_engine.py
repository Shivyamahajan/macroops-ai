
"""
Exception Detection Engine — MacroOps AI
Author: Shivya
Date: October 2026

Detects six operational exception types from the five
source datasets and recommends an action for each exception.
"""

from datetime import datetime
import pandas as pd

from src.analytics.load_data import load_all


def detect_exceptions(limit: int = 500) -> pd.DataFrame:
    """
    Detect operational exceptions across all source datasets.

    Args:
        limit: Maximum number of exception records returned.

    Returns:
        DataFrame containing exception details.
    """
    data = load_all()
    exceptions = []
    detected_at = datetime.now().isoformat(timespec="seconds")

    def add_exception(
        exception_type,
        severity,
        entity_id,
        store_id,
        description,
        recommended_action,
    ):
        exceptions.append(
            {
                "exception_id": f"EXC-{len(exceptions) + 1:06d}",
                "exception_type": exception_type,
                "severity": severity,
                "entity_id": str(entity_id),
                "store_id": str(store_id) if pd.notna(store_id) else "N/A",
                "description": description,
                "recommended_action": recommended_action,
                "status": "Open",
                "detected_at": detected_at,
            }
        )

    # 1. Slow Pick: pick duration > 20 minutes
    picking = data["picking"]
    slow_picks = picking[
        picking["pick_duration_minutes"] > 20
    ]

    for _, row in slow_picks.iterrows():
        order_id = row["order_id"]
        add_exception(
            "Slow Pick",
            "Medium",
            order_id,
            "N/A",
            f"Picking took {row['pick_duration_minutes']:.1f} minutes.",
            "Review picker workload, item locations, and picking delays.",
        )

    # 2. Missing Items: items_missing > 0
    missing_items = picking[picking["items_missing"] > 0]

    for _, row in missing_items.iterrows():
        order_id = row["order_id"]
        add_exception(
            "Missing Items",
            "High",
            order_id,
            "N/A",
            f"{int(row['items_missing'])} item(s) missing from the order.",
            "Verify shelf stock and substitutions; notify the fulfillment team.",
        )

    # 3. High Assignment Delay: delay > 15 minutes
    delivery = data["delivery"]
    delayed_assignments = delivery[
        delivery["assignment_delay_minutes"] > 15
    ]

    for _, row in delayed_assignments.iterrows():
        order_id = row["order_id"]
        add_exception(
            "High Assignment Delay",
            "High",
            order_id,
            "N/A",
            f"Rider assignment took {row['assignment_delay_minutes']:.1f} minutes.",
            "Check rider availability and dispatch queue; rebalance assignments.",
        )

    # 4. Inventory Discrepancy: absolute stock variance > 10
    inventory = data["inventory"]
    discrepancies = inventory[
        inventory["stock_variance"].abs() > 10
    ]

    for _, row in discrepancies.iterrows():
        add_exception(
            "Inventory Discrepancy",
            "High",
            row["sku_id"],
            row["store_id"],
            (
                f"SKU {row['sku_id']} has stock variance "
                f"{row['stock_variance']:+.0f}."
            ),
            "Conduct a physical stock count and reconcile inventory records.",
        )

    # 5. Stockout: stockout == 'Yes'
    stockout_rows = inventory[
        inventory["stockout"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
    ]

    for _, row in stockout_rows.iterrows():
        add_exception(
            "Stockout",
            "Critical",
            row["sku_id"],
            row["store_id"],
            f"SKU {row['sku_id']} is marked as out of stock.",
            "Confirm physical availability and replenish or update stock records.",
        )

    # 6. Overloaded Employee: tasks_pending > 10
    workforce = data["workforce"]
    overloaded = workforce[workforce["tasks_pending"] > 10]

    for _, row in overloaded.iterrows():
        add_exception(
            "Overloaded Employee",
            "Medium",
            row["employee_id"],
            row["store_id"],
            f"Employee has {int(row['tasks_pending'])} pending tasks.",
            "Review workload and redistribute pending tasks where possible.",
        )

    columns = [
        "exception_id",
        "exception_type",
        "severity",
        "entity_id",
        "store_id",
        "description",
        "recommended_action",
        "status",
        "detected_at",
    ]

    result = pd.DataFrame(exceptions, columns=columns)

    # Show the most urgent exceptions first.
    severity_order = {
        "Critical": 0,
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    if not result.empty:
        result["_severity_order"] = result["severity"].map(severity_order)
        result = (
            result.sort_values(
                ["_severity_order", "exception_type"],
                kind="stable",
            )
            .drop(columns="_severity_order")
            .reset_index(drop=True)
        )

        # Assign stable sequential IDs after sorting.
        result["exception_id"] = [
            f"EXC-{i:06d}"
            for i in range(1, len(result) + 1)
        ]

    return result.head(max(0, limit)).copy()


if __name__ == "__main__":
    exceptions = detect_exceptions()

    print("\nEXCEPTION DETECTION SUMMARY")
    print("=" * 40)
    print(f"Exceptions returned: {len(exceptions):,}")

    if exceptions.empty:
        print("No exceptions detected.")
    else:
        print("\nBy exception type:")
        print(exceptions["exception_type"].value_counts().to_string())

        print("\nBy severity:")
        print(exceptions["severity"].value_counts().to_string())

        print("\nFirst 10 exceptions:")
        print(exceptions.head(10).to_string(index=False))
