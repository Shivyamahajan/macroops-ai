
"""
Leakage-safe feature engineering for MacroOps AI SLA risk prediction.
Prediction point: after picking and rider assignment, before delivery.
"""

import pandas as pd

TARGET = "sla_breached"

# Only fields that are available at the prediction point.
FEATURES = [
    "item_count",
    "order_value",
    "order_hour",
    "order_day",
    "is_peak_hour",
    "sla_window_minutes",
    "picking_pick_duration_minutes",
    "picking_items_picked",
    "picking_items_missing",
    "delivery_assignment_delay_minutes",
    "delivery_distance_km",
]

# Outcome fields must never be model inputs.
LEAKY = [
    "actual_delivery_time",
    "status",
    "delivery_delay_minutes",
    "delivery_delivery_time",
    "delivery_pickup_time",
]

REQUIRED_PROCESS_FIELDS = [
    "picking_pick_duration_minutes",
    "delivery_assignment_delay_minutes",
    "delivery_distance_km",
]


def build_ml_table(master: pd.DataFrame):
    """Build the model table using the real master-dataset column names."""
    df = master.copy()

    df["order_time"] = pd.to_datetime(df["order_time"], errors="coerce")
    df["promised_time"] = pd.to_datetime(
        df["promised_time"], errors="coerce"
    )

    # Derive features using information available before delivery completes.
    df["order_hour"] = df["order_time"].dt.hour
    df["order_day"] = df["order_time"].dt.dayofweek
    df["is_peak_hour"] = df["order_hour"].isin([7, 8, 9, 18, 19, 20]).astype(int)
    df["sla_window_minutes"] = (
        df["promised_time"] - df["order_time"]
    ).dt.total_seconds() / 60

    missing_required = [
        col for col in REQUIRED_PROCESS_FIELDS if col not in df.columns
    ]
    if missing_required:
        raise ValueError(f"Required columns missing: {missing_required}")

    available = [col for col in FEATURES if col in df.columns]
    missing_features = [col for col in FEATURES if col not in df.columns]

    if missing_features:
        print("Warning — unavailable features excluded:", missing_features)

    overlap = set(available) & set(LEAKY)
    assert not overlap, f"Potential leakage detected: {overlap}"

    # Keep only orders with the process fields required at prediction time.
    df = df.dropna(subset=REQUIRED_PROCESS_FIELDS + [TARGET])
    df = df.dropna(subset=available + ["order_time", TARGET])
    df = df.sort_values("order_time").reset_index(drop=True)

    if df.empty:
        raise ValueError("No rows remain after feature filtering.")

    result = df[["order_id", "store_id", "order_time"] + available + [TARGET]]

    print(f"ML table: {len(result):,} rows | {len(available)} features")
    print(f"Breach rate: {result[TARGET].mean() * 100:.2f}%")
    print("Features:", available)
    print("\nFeature correlations with SLA breach:")
    print(
        result[available + [TARGET]]
        .corr(numeric_only=True)[TARGET]
        .drop(TARGET)
        .sort_values(key=abs, ascending=False)
        .round(3)
    )

    return result, available


def time_split(df: pd.DataFrame, train=0.70, val=0.10):
    """Chronological 70% train, 10% validation, 20% test split."""
    n = len(df)
    i1 = int(n * train)
    i2 = int(n * (train + val))
    return df.iloc[:i1], df.iloc[i1:i2], df.iloc[i2:]


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.analytics.load_data import load_master

    master = load_master()
    table, features = build_ml_table(master)
    train_df, val_df, test_df = time_split(table)

    print(
        f"\nTrain: {len(train_df):,} | "
        f"Validation: {len(val_df):,} | Test: {len(test_df):,}"
    )
    print(
        f"Train period: {train_df['order_time'].min()} "
        f"to {train_df['order_time'].max()}"
    )
    print(
        f"Test period: {test_df['order_time'].min()} "
        f"to {test_df['order_time'].max()}"
    )
