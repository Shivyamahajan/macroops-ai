"""
Data Loading Utility — MacroOps AI
Author: Shivya
Date: October 2026

Loads all 5 operational datasets and returns them
as clean pandas DataFrames with correct data types.
All other scripts import from this module.
"""

import pandas as pd
import os

# ─── Paths ───
DATA_DIR = "data/dummy"

FILES = {
    "orders": "orders.csv",
    "picking": "picking.csv",
    "delivery": "delivery.csv",
    "inventory": "inventory.csv",
    "workforce": "workforce.csv",
}

# ─── Timestamp columns for each table ───
TIMESTAMP_COLS = {
    "orders": ["order_time", "promised_time", "actual_delivery_time"],
    "picking": ["pick_start", "pick_end"],
    "delivery": ["assignment_time", "pickup_time", "delivery_time"],
    "inventory": [],
    "workforce": [],
}


def load_table(table_name: str) -> pd.DataFrame:
    """
    Load a single table by name and parse timestamps.

    Args:
        table_name: one of 'orders', 'picking', 'delivery',
                    'inventory', 'workforce'

    Returns:
        Clean DataFrame with correct column types
    """
    filepath = os.path.join(DATA_DIR, FILES[table_name])

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset not found: {filepath}\n"
            f"Make sure CSV files are in {DATA_DIR}/"
        )

    df = pd.read_csv(filepath)

    # Parse timestamp columns
    for col in TIMESTAMP_COLS.get(table_name, []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    print(
        f"Loaded {table_name}: "
        f"{len(df):,} rows × {len(df.columns)} columns"
    )

    return df


def load_all() -> dict:
    """
    Load all 5 datasets and return as a dictionary.

    Returns:
        dict with keys: orders, picking, delivery,
                        inventory, workforce
    """
    print("Loading all MacroOps AI datasets...")
    print("=" * 50)

    data = {}

    for name in FILES:
        data[name] = load_table(name)

    total_rows = sum(len(df) for df in data.values())

    print("=" * 50)
    print(f"Total records loaded: {total_rows:,}")

    return data


def load_master() -> pd.DataFrame:
    """
    Load the pre-built master joined dataset.
    Run create_master_dataset.py first to generate it.

    Returns:
        Master operational DataFrame
    """
    master_path = "data/processed/master_operational.csv"

    if not os.path.exists(master_path):
        raise FileNotFoundError(
            "Master dataset not found.\n"
            "Run: python src/analytics/create_master_dataset.py"
        )

    df = pd.read_csv(
        master_path,
        parse_dates=[
            "order_time",
            "promised_time",
            "actual_delivery_time",
        ],
    )

    print(
        f"Loaded master dataset: "
        f"{len(df):,} rows × {len(df.columns)} columns"
    )

    return df


if __name__ == "__main__":
    data = load_all()

    for name, df in data.items():
        print(f"\n{name.upper()} — first 2 rows:")
        print(df.head(2).to_string())