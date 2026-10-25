
"""
Page 1: Operations Overview — MacroOps AI
Author: Shivya
Date: October 2026

Displays operational KPIs, performance charts, store comparisons,
exception summaries, and AI-assisted root-cause insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@st.cache_data(ttl=300)
def load_data():
    """Load and cache operational datasets."""
    from src.analytics.load_data import load_all
    return load_all()


@st.cache_data(ttl=300)
def load_kpis(store_id=None):
    """Calculate operational KPIs using the existing master dataset."""
    from src.analytics.kpi_calculator import calculate_all_kpis
    from src.analytics.create_master_dataset import build_master_dataset

    data = load_data()
    master = build_master_dataset(data)

    return calculate_all_kpis(
        data,
        master,
        store_id=store_id,
    )


@st.cache_data(ttl=300)
def load_exception_summary(store_id=None):
    """Load and summarize detected operational exceptions."""
    from src.analytics.exception_engine import detect_exceptions

    exceptions = detect_exceptions(limit=100000)

    if store_id is not None and not exceptions.empty:
        exceptions = exceptions[
            exceptions["store_id"].astype(str) == str(store_id)
        ]

    severity_counts = (
        exceptions["severity"].value_counts().to_dict()
        if not exceptions.empty
        else {}
    )

    return {
        "total": len(exceptions),
        "high": severity_counts.get("High", 0)
        + severity_counts.get("Critical", 0),
        "medium": severity_counts.get("Medium", 0),
        "low": severity_counts.get("Low", 0),
        "by_type": (
            exceptions["exception_type"].value_counts().to_dict()
            if not exceptions.empty
            else {}
        ),
    }


def render_kpi_card(label, value, unit, status, detail=""):
    """Display a styled KPI card."""
    colors = {
        "good": "#16A34A",
        "warning": "#D97706",
        "critical": "#DC2626",
        "neutral": "#2563EB",
    }
    color = colors.get(status, "#2563EB")

    st.markdown(
        f"""
        <div style="
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid {color};
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            min-height: 105px;
            margin-bottom: 8px;
        ">
            <div style="font-size: 0.8rem; color: #666;">
                {label}
            </div>
            <div style="font-size: 1.6rem; font-weight: bold;
                        color: {color};">
                {value}
                <span style="font-size: 0.8rem; font-weight: normal;">
                    {unit}
                </span>
            </div>
            <div style="font-size: 0.72rem; color: #888;">
                {detail}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render(store_id=None):
    """Render the Operations Overview page."""
    title = (
        f"Operations Overview — {store_id}"
        if store_id
        else "Operations Overview — All Stores"
    )

    st.title(f"🏠 {title}")
    st.caption(
        "Operational intelligence | MacroOps AI | "
        "Data refreshes every 5 minutes"
    )
    st.info(
        "This project currently uses synthetic demonstration data. "
        "The dashboard does not represent live operations."
    )

    with st.spinner("Loading operational data..."):
        data = load_data()
        kpis = load_kpis(store_id)
        exc_sum = load_exception_summary(store_id)

    orders = data["orders"].copy()
    picking = data["picking"].copy()
    delivery = data["delivery"].copy()
    inventory = data["inventory"].copy()

    if store_id:
        orders = orders[orders["store_id"] == store_id]
        order_ids = set(orders["order_id"])

        picking = picking[picking["order_id"].isin(order_ids)]
        delivery = delivery[delivery["order_id"].isin(order_ids)]
        inventory = inventory[inventory["store_id"] == store_id]

    st.subheader("📊 Key Performance Indicators")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        k = kpis["order_volume"]
        render_kpi_card(
            "Total Orders", f'{k["value"]:,}',
            k["unit"], k["status"], k.get("detail", "")
        )

    with c2:
        k = kpis["sla_breach_rate"]
        render_kpi_card(
            "SLA Breach Rate", k["value"],
            k["unit"], k["status"], k.get("detail", "")
        )

    with c3:
        render_kpi_card(
            "Active Exceptions",
            exc_sum["total"],
            "exceptions",
            "critical" if exc_sum["high"] > 10
            else "warning" if exc_sum["total"] > 5
            else "good",
            f'High: {exc_sum["high"]} | Medium: {exc_sum["medium"]}',
        )

    with c4:
        k = kpis["avg_pick_duration"]
        render_kpi_card(
            "Avg Pick Duration", k["value"],
            k["unit"], k["status"], k.get("detail", "")
        )

    with c5:
        k = kpis["avg_assignment_delay"]
        render_kpi_card(
            "Avg Assignment Delay", k["value"],
            k["unit"], k["status"], k.get("detail", "")
        )

    with c6:
        k = kpis["inventory_accuracy"]
        render_kpi_card(
            "Inventory Accuracy", k["value"],
            k["unit"], k["status"], k.get("detail", "")
        )

    st.divider()
    st.subheader("📈 Order Performance")

    left, right = st.columns([1, 2])

    with left:
        status_counts = orders["status"].value_counts()

        fig = go.Figure(
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=0.55,
            )
        )
        fig.update_layout(
            title="Order Status Distribution",
            height=320,
        )
        st.plotly_chart(fig, width="stretch")

    with right:
        orders["order_time"] = pd.to_datetime(
            orders["order_time"]
        )
        orders["order_hour"] = orders["order_time"].dt.hour

        hourly = orders.groupby("order_hour").agg(
            total=("order_id", "count"),
            breached=("sla_breached", "sum"),
        ).reset_index()

        hourly["breach_rate"] = (
            hourly["breached"] / hourly["total"] * 100
        )

        fig = px.bar(
            hourly,
            x="order_hour",
            y="breach_rate",
            title="SLA Breach Rate by Hour",
            labels={
                "order_hour": "Hour of Day",
                "breach_rate": "SLA Breach Rate (%)",
            },
        )
        fig.update_layout(height=320)
        st.plotly_chart(fig, width="stretch")

    st.divider()
    st.subheader("🏪 Store Performance Comparison")

    store_perf = orders.groupby("store_id").agg(
        total_orders=("order_id", "count"),
        breach_count=("sla_breached", "sum"),
        avg_delay=("delivery_delay_minutes", "mean"),
    ).reset_index()

    store_perf["breach_rate"] = (
        store_perf["breach_count"]
        / store_perf["total_orders"] * 100
    )

    worst, best = st.columns(2)

    with worst:
        worst_10 = store_perf.nlargest(10, "breach_rate")
        fig = px.bar(
            worst_10,
            x="breach_rate",
            y="store_id",
            orientation="h",
            title="10 Worst Stores — SLA Breach Rate",
            labels={"breach_rate": "Breach Rate (%)"},
        )
        st.plotly_chart(fig, width="stretch")

    with best:
        best_10 = store_perf.nsmallest(10, "breach_rate")
        fig = px.bar(
            best_10,
            x="breach_rate",
            y="store_id",
            orientation="h",
            title="10 Best Stores — SLA Breach Rate",
            labels={"breach_rate": "Breach Rate (%)"},
        )
        st.plotly_chart(fig, width="stretch")

    st.divider()
    st.subheader("🔄 Picking and Delivery Performance")

    pick_col, delivery_col = st.columns(2)

    with pick_col:
        if not picking.empty:
            fig = px.histogram(
                picking,
                x="pick_duration_minutes",
                nbins=40,
                title="Pick Duration Distribution",
            )
            st.plotly_chart(fig, width="stretch")

    with delivery_col:
        if not delivery.empty:
            fig = px.histogram(
                delivery,
                x="assignment_delay_minutes",
                nbins=35,
                title="Rider Assignment Delay Distribution",
            )
            st.plotly_chart(fig, width="stretch")

    st.divider()
    st.subheader("⚠️ Exception Overview")

    e1, e2, e3 = st.columns(3)
    e1.metric("High Severity", exc_sum["high"])
    e2.metric("Medium Severity", exc_sum["medium"])
    e3.metric("Low Severity", exc_sum["low"])

    if exc_sum.get("by_type"):
        type_df = pd.DataFrame(
            list(exc_sum["by_type"].items()),
            columns=["Exception Type", "Count"],
        )

        fig = px.bar(
            type_df,
            x="Count",
            y="Exception Type",
            orientation="h",
            title="Exceptions by Type",
        )
        st.plotly_chart(fig, width="stretch")

    st.caption(
        "Review individual exceptions in the Exception Management page."
    )

    # Reuse the existing root-cause insights module.
    try:
        from src.ai.root_cause_insights import (
            generate_root_cause_insights,
        )

        st.divider()
        st.subheader("🤖 AI-Assisted Root-Cause Insights")
        st.caption(
            "These are rule-based hypotheses for investigation, "
            "not confirmed causes."
        )

        insights = generate_root_cause_insights(limit=100)

        if not insights.empty:
            columns = [
                col for col in [
                    "exception_type",
                    "severity",
                    "entity_id",
                    "likely_cause",
                    "investigation",
                ]
                if col in insights.columns
            ]
            st.dataframe(
                insights[columns],
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("No root-cause insights are available.")

    except (ImportError, KeyError, ValueError) as exc:
        st.warning(f"Root-cause insights could not be loaded: {exc}")

render()
