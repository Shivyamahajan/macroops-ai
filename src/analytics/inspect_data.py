
import sys
sys.path.insert(0, ".")

from src.analytics.load_data import load_all

data = load_all()

for name, df in data.items():
    print("\n" + "=" * 70)
    print(f"TABLE: {name.upper()}")
    print("=" * 70)

    print("\nColumn names and data types:")
    print(df.dtypes.to_string())

    print("\nNumeric summary:")
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        print(numeric.describe().round(2).to_string())

    print("\nUnique values in categorical columns:")
    for col in df.select_dtypes(include=["object", "string"]).columns:
        unique_values = df[col].nunique(dropna=True)
        print(f"\n{col}: {unique_values} unique values")

        if unique_values <= 20:
            print(df[col].value_counts(dropna=False).to_string())
