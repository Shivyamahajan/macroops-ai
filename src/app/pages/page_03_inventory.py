"""
Page 3: Inventory Status — MacroOps AI
Author: Shivya
Date: October 2026

Shows real-time inventory accuracy, discrepancies, stockouts,
and store-level inventory health.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append('.')


@st.cache_data(ttl=300)
def load_inventory_data():
    from src.analytics.load_data import load_all
    data = load_all()
    return data['inventory']


def render(store_id: str = None):
    """Render the Inventory Status page."""

    title = (
        f"Inventory Status — {store_id}"
        if store_id else "Inventory Status — All Stores"
    )
    st.markdown(
        f'<div class="main-header">📦 {title}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">Real-time inventory accuracy, '
        'discrepancy detection, and stockout monitoring</div>',
        unsafe_allow_html=True
    )

    inventory = load_inventory_data()

    if store_id:
        inventory = inventory[inventory['store_id'] == store_id]
        if inventory.empty:
            st.warning(f"No inventory data found for {store_id}")
            return

    # ═══════════════════════════════════
    # TOP KPI CARDS
    # ═══════════════════════════════════
    st.markdown("### 📊 Inventory KPIs")

    avg_acc     = inventory['inventory_accuracy_pct'].mean()
    stockouts   = (inventory['stockout'] == 'Yes').sum()
    neg_var     = (inventory['stock_variance'] < 0).sum()
    high_var    = (inventory['stock_variance'].abs() > 10).sum()
    low_acc_cnt = (inventory['inventory_accuracy_pct'] < 80).sum()
    total_skus  = inventory['sku_id'].nunique()

    def acc_status(val):
        if val >= 95: return '🟢'
        elif val >= 85: return '🟡'
        else: return '🔴'

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        color = ('#16A34A' if avg_acc >= 95 else
                 '#D97706' if avg_acc >= 85 else '#DC2626')
        st.markdown(f"""
        <div style="background:white; padding:1rem;
                    border-radius:8px; border-left:5px solid {color};
                    box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <p style="margin:0;font-size:0.78rem;color:#666;">
                Avg Inventory Accuracy</p>
            <p style="margin:0;font-size:1.6rem;
                      font-weight:bold;color:{color};">
                {avg_acc:.1f}%</p>
            <p style="margin:0;font-size:0.7rem;color:#999;">
                Target: ≥ 95%</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        color2 = '#DC2626' if stockouts > 0 else '#16A34A'
        st.markdown(f"""
        <div style="background:white; padding:1rem;
                    border-radius:8px; border-left:5px solid {color2};
                    box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <p style="margin:0;font-size:0.78rem;color:#666;">
                Complete Stockouts</p>
            <p style="margin:0;font-size:1.6rem;
                      font-weight:bold;color:{color2};">
                {stockouts}</p>
            <p style="margin:0;font-size:0.7rem;color:#999;">
                Target: 0</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        color3 = '#D97706' if neg_var > 100 else '#16A34A'
        st.markdown(f"""
        <div style="background:white; padding:1rem;
                    border-radius:8px; border-left:5px solid {color3};
                    box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <p style="margin:0;font-size:0.78rem;color:#666;">
                Negative Variance Items</p>
            <p style="margin:0;font-size:1.6rem;
                      font-weight:bold;color:{color3};">
                {neg_var:,}</p>
            <p style="margin:0;font-size:0.7rem;color:#999;">
                Physical &lt; System</p>
        </div>""", unsafe_allow_html=True)
    with c4:
        color4 = '#D97706' if high_var > 200 else '#16A34A'
        st.markdown(f"""
        <div style="background:white; padding:1rem;
                    border-radius:8px; border-left:5px solid {color4};
                    box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <p style="margin:0;font-size:0.78rem;color:#666;">
                High Variance Items (&gt;10)</p>
            <p style="margin:0;font-size:1.6rem;
                      font-weight:bold;color:{color4};">
                {high_var:,}</p>
            <p style="margin:0;font-size:0.7rem;color:#999;">
                Target: &lt; 100</p>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div style="background:white; padding:1rem;
                    border-radius:8px; border-left:5px solid #2563EB;
                    box-shadow:0 1px 3px rgba(0,0,0,0.1);">
            <p style="margin:0;font-size:0.78rem;color:#666;">
                Total SKUs Monitored</p>
            <p style="margin:0;font-size:1.6rem;
                      font-weight:bold;color:#2563EB;">
                {total_skus:,}</p>
            <p style="margin:0;font-size:0.7rem;color:#999;">
                Across {inventory['store_id'].nunique()} stores</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ═══════════════════════════════════
    # STOCKOUT ALERT BOX
    # ═══════════════════════════════════
    if stockouts > 0:
        st.error(f"🚨 **CRITICAL: {stockouts} Complete Stockout(s) Detected**")
        stockout_items = inventory[inventory['stockout'] == 'Yes'][[
            'store_id', 'sku_id', 'system_stock', 'physical_stock'
        ]]
        st.dataframe(stockout_items.reset_index(drop=True),
                     use_container_width=True)
        st.markdown("---")

    # ═══════════════════════════════════
    # ACCURACY DISTRIBUTION
    # ═══════════════════════════════════
    st.markdown("### 📈 Inventory Accuracy Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(
            inventory,
            x='inventory_accuracy_pct',
            nbins=30,
            title='Inventory Accuracy Distribution',
            color_discrete_sequence=['#2563EB'],
            labels={'inventory_accuracy_pct': 'Accuracy (%)',
                    'count': 'SKU-Store Records'}
        )
        fig_hist.add_vline(
            x=inventory['inventory_accuracy_pct'].mean(),
            line_dash="dash", line_color="red",
            annotation_text=f"Avg: {avg_acc:.1f}%"
        )
        fig_hist.add_vline(
            x=80, line_dash="dot", line_color="orange",
            annotation_text="Alert: 80%"
        )
        fig_hist.add_vline(
            x=95, line_dash="dot", line_color="green",
            annotation_text="Target: 95%"
        )
        fig_hist.update_layout(
            height=320,
            margin=dict(t=50, b=30, l=50, r=30)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        fig_var = px.histogram(
            inventory,
            x='stock_variance',
            nbins=40,
            title='Stock Variance Distribution',
            color_discrete_sequence=['#7C3AED'],
            labels={'stock_variance': 'Variance (Physical - System)',
                    'count': 'Records'}
        )
        fig_var.add_vline(x=0, line_color="black", line_width=2,
                           annotation_text="Zero (perfect)")
        fig_var.add_vline(x=10, line_dash="dot",
                           line_color="orange",
                           annotation_text="+10 threshold")
        fig_var.add_vline(x=-10, line_dash="dot",
                           line_color="red",
                           annotation_text="-10 threshold")
        fig_var.update_layout(
            height=320,
            margin=dict(t=50, b=30, l=50, r=30)
        )
        st.plotly_chart(fig_var, use_container_width=True)

    st.markdown("---")

    # ═══════════════════════════════════
    # STORE-LEVEL ACCURACY TABLE
    # ═══════════════════════════════════
    st.markdown("### 🏪 Store-Level Inventory Health")

    store_inv = inventory.groupby('store_id').agg(
        avg_accuracy      = ('inventory_accuracy_pct', 'mean'),
        min_accuracy      = ('inventory_accuracy_pct', 'min'),
        stockout_count    = ('stockout',
                             lambda x: (x=='Yes').sum()),
        high_var_count    = ('stock_variance',
                             lambda x: (x.abs()>10).sum()),
        neg_var_count     = ('stock_variance',
                             lambda x: (x<0).sum()),
        total_skus        = ('sku_id', 'count'),
    ).reset_index().sort_values('avg_accuracy')

    store_inv['avg_accuracy'] = store_inv['avg_accuracy'].round(1)
    store_inv['min_accuracy'] = store_inv['min_accuracy'].round(1)

    store_inv['Health'] = store_inv['avg_accuracy'].apply(
        lambda x: '🔴 Critical' if x < 80 else
                  '🟡 Warning' if x < 90 else '🟢 Good'
    )

    st.markdown("**Filter stores by accuracy:**")
    threshold_filter = st.slider(
        "Show stores with avg accuracy BELOW:",
        min_value=80, max_value=100, value=95, step=5
    )

    filtered_stores = store_inv[
        store_inv['avg_accuracy'] < threshold_filter
    ]
    st.markdown(
        f"**{len(filtered_stores)} stores** with avg accuracy "
        f"below {threshold_filter}%"
    )

    st.dataframe(
        filtered_stores.rename(columns={
            'store_id':       'Store',
            'avg_accuracy':   'Avg Accuracy %',
            'min_accuracy':   'Min Accuracy %',
            'stockout_count': 'Stockouts',
            'high_var_count': 'High Variance',
            'neg_var_count':  'Shortage Items',
            'total_skus':     'Total SKUs',
        }).reset_index(drop=True),
        use_container_width=True,
        height=400
    )

    # ═══════════════════════════════════
    # TOP PROBLEM SKUs
    # ═══════════════════════════════════
    st.markdown("---")
    st.markdown("### 🔍 Worst Performing SKUs")

    sku_perf = inventory.groupby('sku_id').agg(
        avg_accuracy  = ('inventory_accuracy_pct', 'mean'),
        stores_affected= ('store_id', 'count'),
        total_neg_var  = ('stock_variance',
                          lambda x: (x < 0).sum()),
    ).reset_index().sort_values('avg_accuracy').head(20)
    sku_perf['avg_accuracy'] = sku_perf['avg_accuracy'].round(1)

    fig_sku = px.bar(
        sku_perf.head(15),
        x='avg_accuracy', y='sku_id',
        orientation='h',
        title='15 SKUs with Lowest Average Accuracy',
        color='avg_accuracy',
        color_continuous_scale='Reds_r',
        labels={'avg_accuracy': 'Avg Accuracy %',
                'sku_id': 'SKU'}
    )
    fig_sku.add_vline(x=80, line_dash="dot",
                       line_color="orange",
                       annotation_text="80% alert")
    fig_sku.update_layout(
        height=450,
        margin=dict(t=50, b=30, l=80, r=30),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_sku, use_container_width=True)

render()