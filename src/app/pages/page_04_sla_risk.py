
"""
Page 4: SLA Risk Monitor — MacroOps AI
Author: Shivya | October 2026

Scores held-out test-period orders to demonstrate how SLA risk
prediction would work on live orders. These are historical
demonstration predictions, not live predictions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys

sys.path.insert(0, ".")

TIER_COLOR = {
    "High": "#DC2626",
    "Medium": "#D97706",
    "Low": "#16A34A",
}


@st.cache_resource
def get_predictor():
    from src.ai.sla_predictor import SLAPredictor
    return SLAPredictor()


@st.cache_data(ttl=600)
def get_scored(max_rows=5000):
    from src.analytics.load_data import load_master
    from src.ai.feature_engineering import build_ml_table, time_split

    master = load_master()
    table, _ = build_ml_table(master)
    _, _, test = time_split(table)

    predictor = get_predictor()
    scored = predictor.score(test.tail(max_rows))

    return scored


@st.cache_data(ttl=600)
def get_background(max_rows=500):
    from src.analytics.load_data import load_master
    from src.ai.feature_engineering import build_ml_table, time_split

    master = load_master()
    table, _ = build_ml_table(master)
    train, _, _ = time_split(table)

    return train.sample(
        n=min(max_rows, len(train)),
        random_state=42
    )


def render(store_id: str = None):
    st.markdown(
        '<div class="main-header">🔮 SLA Risk Monitor</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">Machine-learning breach risk '
        'with per-order explanations</div>',
        unsafe_allow_html=True
    )

    try:
        predictor = get_predictor()
        scored = get_scored()
        background = get_background()

    except FileNotFoundError as error:
        st.error(f"Required file not found: {error}")
        st.info(
            "Check that the master dataset and trained model "
            "are available."
        )
        return

    except Exception as error:
        st.error(f"Unable to load SLA risk data: {error}")
        return

    st.info(
        "**Historical demonstration mode:** Orders shown here come "
        "from the held-out test period of the historical dataset. "
        "They are scored to demonstrate how the model could work "
        "on live orders. These are not live or real-time predictions. "
        f"Model: **{predictor.name}**. "
        "Risk tiers use thresholds selected on the validation data."
    )

    if store_id:
        scored = scored[scored["store_id"] == store_id]

        if scored.empty:
            st.warning(f"No scored orders found for {store_id}.")
            return

    if scored.empty:
        st.warning("No orders are available for scoring.")
        return

    # Summary metrics
    st.markdown("### 📊 Risk Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Orders scored", f"{len(scored):,}")
    c2.metric(
        "🔴 High risk",
        int((scored["risk_tier"] == "High").sum())
    )
    c3.metric(
        "🟡 Medium risk",
        int((scored["risk_tier"] == "Medium").sum())
    )
    c4.metric(
        "🟢 Low risk",
        int((scored["risk_tier"] == "Low").sum())
    )

    st.caption(
        f"Historical test period: "
        f"{scored['order_time'].min():%d %b %Y} – "
        f"{scored['order_time'].max():%d %b %Y}"
    )

    st.markdown("---")

    # Risk visualizations
    col_a, col_b = st.columns([1, 2])

    with col_a:
        tier_counts = (
            scored["risk_tier"]
            .value_counts()
            .reindex(["High", "Medium", "Low"], fill_value=0)
            .rename_axis("Tier")
            .reset_index(name="Count")
        )

        fig = px.pie(
            tier_counts,
            names="Tier",
            values="Count",
            hole=0.5,
            color="Tier",
            color_discrete_map=TIER_COLOR,
            title="Risk Tier Distribution"
        )

        fig.update_layout(
            height=320,
            margin=dict(t=50, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = px.histogram(
            scored,
            x="risk_probability",
            nbins=40,
            color="risk_tier",
            color_discrete_map=TIER_COLOR,
            title="Predicted SLA Breach Probability",
            labels={
                "risk_probability": "Predicted breach probability",
                "count": "Number of orders",
            }
        )

        fig2.update_layout(
            height=320,
            margin=dict(t=50, b=10)
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Highest-risk orders
    st.markdown("### 🚨 Highest-Risk Orders")

    selected_tiers = st.multiselect(
        "Filter by risk tier",
        ["High", "Medium", "Low"],
        default=["High"]
    )

    shown = (
        scored[scored["risk_tier"].isin(selected_tiers)]
        .sort_values("risk_probability", ascending=False)
        .head(100)
    )

    if shown.empty:
        st.caption("No orders match the selected risk tiers.")
        return

    display_columns = [
        "order_id",
        "store_id",
        "risk_probability",
        "risk_tier",
        "picking_pick_duration_minutes",
        "delivery_assignment_delay_minutes",
        "delivery_distance_km",
    ]

    display_names = {
        "order_id": "Order ID",
        "store_id": "Store",
        "risk_probability": "Breach Probability",
        "risk_tier": "Risk Tier",
        "picking_pick_duration_minutes": "Picking Time (min)",
        "delivery_assignment_delay_minutes": "Assignment Delay (min)",
        "delivery_distance_km": "Distance (km)",
    }

    st.dataframe(
        shown[display_columns]
        .rename(columns=display_names)
        .round(3)
        .reset_index(drop=True),
        use_container_width=True,
        height=350
    )

    # Individual order explanation
    st.markdown("### 🔍 Why Is This Order at Risk?")

    chosen = st.selectbox(
        "Select an order to investigate",
        shown["order_id"].tolist()
    )

    row = (
        scored[scored["order_id"] == chosen]
        .head(1)
    )

    probability = float(row["risk_probability"].iloc[0])

    st.progress(
        min(max(probability, 0.0), 1.0),
        text=f"Predicted breach probability: {probability:.1%}"
    )

    try:
        factors = predictor.explain(
            row,
            background,
            top_n=3
        )

    except Exception as error:
        st.warning(f"Unable to generate SHAP explanation: {error}")
        return

    st.markdown("**Top contributing factors**")

    for factor in factors:
        icon = "🔺" if factor["shap"] > 0 else "🔻"
        st.markdown(f"{icon} {factor['text']}")

    actions = [
        factor["action"]
        for factor in factors
        if factor["action"]
    ]

    if actions:
        st.success(
            "**Suggested operational actions:** "
            + " ".join(actions[:2])
        )
    else:
        st.caption(
            "No specific corrective action maps to these factors."
        )

    # Historical outcome for demonstration and evaluation
    actual = int(row["sla_breached"].iloc[0])

    st.caption(
        "Historical ground truth: "
        + ("SLA breached" if actual else "Delivered on time")
    )


render()
