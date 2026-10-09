
"""
Data Quality Report — MacroOps AI
Author: Shivya
Date: October 2026

Checks missing values, duplicate rows, and basic
logical consistency across all five datasets.
"""

import pandas as pd
import sys
sys.path.insert(0, ".")
from src.analytics.load_data import load_all


def check_table_quality(name: str, df: pd.DataFrame) -> dict:
    """Check basic data quality for one dataset."""

    result = {
        "table": name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_total": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "findings": [],
    }

    # Check missing values in each column.
    for col, count in df.isnull().sum().items():
        if count > 0:
            pct = count / len(df) * 100
            result["findings"].append(
                f"MISSING: {col}: {count} ({pct:.2f}%)"
            )

    # Check duplicate complete rows.
    if result["duplicate_rows"] > 0:
        result["findings"].append(
            f"DUPLICATES: {result['duplicate_rows']} duplicate rows"
        )

    # Table-specific checks.
    if name == "orders":
        invalid_time = (
            df["actual_delivery_time"] < df["order_time"]
        ).sum()

        if invalid_time > 0:
            result["findings"].append(
                f"TIME CHECK: {invalid_time} records have "
                "actual_delivery_time before order_time"
            )

        inconsistent_status = (
            (df["status"] == "Delivered_Late")
            & (df["sla_breached"] == 0)
        ).sum()

        if inconsistent_status > 0:
            result["findings"].append(
                f"SLA CHECK: {inconsistent_status} records are "
                "Delivered_Late but have sla_breached = 0"
            )

        negative_delay = (
            df["delivery_delay_minutes"] < 0
        ).sum()

        if negative_delay > 0:
            result["findings"].append(
                f"NEGATIVE DELAY: {negative_delay} records"
            )

    elif name == "picking":
        invalid_duration = (
            df["pick_duration_minutes"] <= 0
        ).sum()

        if invalid_duration > 0:
            result["findings"].append(
                f"INVALID DURATION: {invalid_duration} records"
            )

        invalid_items = (
            (df["items_picked"] < 0)
            | (df["items_missing"] < 0)
        ).sum()

        if invalid_items > 0:
            result["findings"].append(
                f"INVALID ITEM COUNTS: {invalid_items} records"
            )

    elif name == "inventory":
        negative_stock = (
            (df["system_stock"] < 0)
            | (df["physical_stock"] < 0)
        ).sum()

        if negative_stock > 0:
            result["findings"].append(
                f"NEGATIVE STOCK: {negative_stock} records"
            )

        expected_variance = (
            df["physical_stock"] - df["system_stock"]
        )

        mismatch = (
            expected_variance != df["stock_variance"]
        ).sum()

        if mismatch > 0:
            result["findings"].append(
                f"VARIANCE CHECK: {mismatch} mismatched records"
            )

    elif name == "workforce":
        negative_tasks = (
            (df["tasks_completed"] < 0)
            | (df["tasks_pending"] < 0)
        ).sum()

        if negative_tasks > 0:
            result["findings"].append(
                f"NEGATIVE TASK COUNTS: {negative_tasks} records"
            )

    if not result["findings"]:
        result["findings"].append(
            "No issues detected by these checks."
        )

    return result


def main():
    data = load_all()
    total_issues = 0

    print("\n" + "=" * 65)
    print("DATA QUALITY REPORT — MACROOPS AI")
    print("=" * 65)

    for name, df in data.items():
        result = check_table_quality(name, df)

        print(f"\nTABLE: {name.upper()}")
        print(
            f"Rows: {result['rows']:,} | "
            f"Columns: {result['columns']} | "
            f"Missing: {result['missing_total']} | "
            f"Duplicate rows: {result['duplicate_rows']}"
        )

        for finding in result["findings"]:
            print(f"  - {finding}")

            if not finding.startswith("No issues detected"):
                total_issues += 1

    print("\n" + "=" * 65)
    print(f"Total reported findings: {total_issues}")
    print("Note: findings require interpretation; not all are errors.")
    print("=" * 65)


if __name__ == "__main__":
    main()
