
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.analytics.load_data import load_all
from src.analytics.exception_engine import detect_exceptions
from src.ai.root_cause_insights import generate_root_cause_insights

st.set_page_config(
    page_title="Operations Overview | MacroOps AI",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Operations Overview")
st.caption("Key performance indicators for quick-commerce operations")

@st.cache_data
def get_operational_data():
    return load_all()

@st.cache_data
def get_exceptions():
    # Retrieve all detected exceptions for accurate summary counts.
    return detect_exceptions(limit=100000)

@st.cache_data
def get_root_cause_insights():
    return generate_root_cause_insights(limit=100000)

data = get_operational_data()
orders = data["orders"]
picking = data["picking"]
inventory = data["inventory"]

exceptions = get_exceptions()
root_cause_insights = get_root_cause_insights()

total_orders = len(orders)
delivered = orders[
    orders["status"].astype(str).str.startswith("Delivered")
]
delivered_count = len(delivered)

if delivered_count:
    on_time_rate = (
        delivered["status"].eq("Delivered_On_Time").mean() * 100
    )
    sla_breach_rate = (
        delivered["sla_breached"].astype(int).mean() * 100
    )
else:
    on_time_rate = 0
    sla_breach_rate = 0

avg_pick_time = picking["pick_duration_minutes"].mean()
inventory_accuracy = inventory["inventory_accuracy_pct"].mean()

st.subheader("Operational KPIs")

c1, c2, c3 = st.columns(3)
c1.metric("Total Orders", f"{total_orders:,}")
c2.metric("Delivered Orders", f"{delivered_count:,}")
c3.metric("On-Time Delivery Rate", f"{on_time_rate:.2f}%")

c4, c5, c6 = st.columns(3)
c4.metric("SLA Breach Rate", f"{sla_breach_rate:.2f}%")
c5.metric("Average Pick Time", f"{avg_pick_time:.2f} min")
c6.metric("Inventory Accuracy", f"{inventory_accuracy:.2f}%")

st.divider()

st.subheader("Exception Summary")

if exceptions.empty:
    st.success("No exceptions detected.")
else:
    left, right = st.columns(2)

    with left:
        st.metric("Total Exceptions", f"{len(exceptions):,}")

        type_counts = (
            exceptions["exception_type"]
            .value_counts()
            .rename_axis("Exception Type")
            .reset_index(name="Count")
        )

        st.bar_chart(
            type_counts,
            x="Exception Type",
            y="Count",
        )

    with right:
        st.markdown("#### Exceptions by Severity")

        severity_order = ["Critical", "High", "Medium", "Low"]
        severity_counts = (
            exceptions["severity"]
            .value_counts()
            .reindex(severity_order, fill_value=0)
            .rename_axis("Severity")
            .reset_index(name="Count")
        )

        st.bar_chart(
            severity_counts,
            x="Severity",
            y="Count",
        )

st.divider()

st.subheader("AI-Assisted Root-Cause Insights")

if root_cause_insights.empty:
    st.info("No root-cause insights available.")
else:
    st.caption(
        "These are rule-based hypotheses to guide investigation, "
        "not confirmed root causes."
    )

    display_columns = [
        "exception_type",
        "severity",
        "entity_id",
        "likely_cause",
        "investigation",
    ]

    st.dataframe(
        root_cause_insights[display_columns],
        width="stretch",
        hide_index=True,
    )

st.caption(
    "Data source: MacroOps AI synthetic operational datasets. "
    "Metrics reflect the current dataset, not live production operations."
)
