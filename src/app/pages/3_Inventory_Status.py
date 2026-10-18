
import streamlit as st
import pandas as pd

from src.analytics.load_data import load_all

st.set_page_config(
    page_title="Inventory Status | MacroOps AI",
    page_icon="📦",
    layout="wide",
)

st.title("📦 Inventory Status")
st.caption(
    "Monitor inventory accuracy, stock discrepancies, and stockout risks."
)


@st.cache_data
def load_inventory():
    data = load_all()
    return data["inventory"].copy()


inventory = load_inventory()

if inventory.empty:
    st.warning("No inventory records are available.")
    st.stop()

# Prepare inventory data
inventory["stock_variance"] = pd.to_numeric(
    inventory["stock_variance"], errors="coerce"
)
inventory["inventory_accuracy_pct"] = pd.to_numeric(
    inventory["inventory_accuracy_pct"], errors="coerce"
)

if "stockout" in inventory.columns:
    inventory["stockout"] = (
        inventory["stockout"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

# Inventory KPIs
total_records = len(inventory)
avg_accuracy = inventory["inventory_accuracy_pct"].mean()
discrepancy_count = (
    inventory["stock_variance"].abs() > 10
).sum()

if "stockout" in inventory.columns:
    stockout_count = inventory["stockout"].eq("yes").sum()
else:
    stockout_count = 0

st.subheader("Inventory KPIs")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Inventory Records", f"{total_records:,}")
c2.metric("Average Inventory Accuracy", f"{avg_accuracy:.2f}%")
c3.metric("Significant Discrepancies", f"{discrepancy_count:,}")
c4.metric("Stockout Records", f"{stockout_count:,}")

st.divider()

# Variance analysis
st.subheader("Stock Variance Analysis")

left, right = st.columns(2)

with left:
    st.markdown("#### Variance Distribution")

    variance_data = (
        inventory["stock_variance"]
        .dropna()
        .round()
        .value_counts()
        .sort_index()
        .rename_axis("Stock Variance")
        .reset_index(name="Records")
    )

    st.bar_chart(
        variance_data,
        x="Stock Variance",
        y="Records",
    )

with right:
    st.markdown("#### Discrepancy Breakdown")

    variance = inventory["stock_variance"]

    breakdown = pd.DataFrame({
        "Category": [
            "Negative variance",
            "No variance",
            "Positive variance",
        ],
        "Records": [
            (variance < 0).sum(),
            (variance == 0).sum(),
            (variance > 0).sum(),
        ],
    })

    st.bar_chart(
        breakdown,
        x="Category",
        y="Records",
    )

st.divider()

# Filters
st.subheader("Inventory Records")

f1, f2 = st.columns(2)

with f1:
    variance_filter = st.selectbox(
        "Filter by variance",
        [
            "All records",
            "Significant discrepancy (> 10 units)",
            "Negative variance",
            "Positive variance",
            "Zero variance",
        ],
    )

with f2:
    if "stockout" in inventory.columns:
        stockout_filter = st.selectbox(
            "Filter by stockout status",
            ["All records", "Stockout only", "No stockout"],
        )
    else:
        stockout_filter = "All records"

filtered = inventory.copy()

if variance_filter == "Significant discrepancy (> 10 units)":
    filtered = filtered[
        filtered["stock_variance"].abs() > 10
    ]
elif variance_filter == "Negative variance":
    filtered = filtered[filtered["stock_variance"] < 0]
elif variance_filter == "Positive variance":
    filtered = filtered[filtered["stock_variance"] > 0]
elif variance_filter == "Zero variance":
    filtered = filtered[filtered["stock_variance"] == 0]

if "stockout" in filtered.columns:
    if stockout_filter == "Stockout only":
        filtered = filtered[filtered["stockout"] == "yes"]
    elif stockout_filter == "No stockout":
        filtered = filtered[filtered["stockout"] != "yes"]

st.write(f"Matching inventory records: **{len(filtered):,}**")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download filtered inventory as CSV",
    data=csv_data,
    file_name="macroops_inventory_status.csv",
    mime="text/csv",
)

st.caption(
    "Data source: MacroOps AI synthetic inventory dataset. "
    "Significant discrepancy is defined here as an absolute stock variance greater than 10 units."
)
