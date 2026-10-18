
"""
MacroOps AI — Operations Dashboard
Main application and navigation.
"""

import streamlit as st

st.set_page_config(
    page_title="MacroOps AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("📦 MacroOps AI")
st.sidebar.caption("Quick-Commerce Operations Intelligence")
st.sidebar.divider()

st.sidebar.markdown("### Navigation")
st.sidebar.page_link(
    "app.py",
    label="Operations Overview",
    icon="📊",
)
st.sidebar.page_link(
    "pages/1_Operations_Overview.py",
    label="Operations Overview Page",
    icon="🏠",
)
st.sidebar.page_link(
    "pages/2_Exception_Management.py",
    label="Exception Management",
    icon="🚨",
)
st.sidebar.page_link(
    "pages/3_Inventory_Status.py",
    label="Inventory Status",
    icon="📦",
)

st.title("📦 MacroOps AI")
st.subheader("Quick-Commerce Operations Intelligence Platform")

st.markdown(
    """
    Welcome to MacroOps AI, an operations intelligence platform designed
    to help quick-commerce teams monitor fulfillment, delivery, inventory,
    and workforce performance.
    """
)

st.info(
    "Dashboard setup is in progress. Use the sidebar to navigate "
    "between Operations Overview, Exception Management, and Inventory Status."
)

st.markdown("### Platform Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📊 Operations Overview")
    st.write("Monitor key operational performance indicators.")

with col2:
    st.markdown("#### 🚨 Exception Management")
    st.write("Review detected exceptions and recommended actions.")

with col3:
    st.markdown("#### 📦 Inventory Status")
    st.write("Monitor stock discrepancies and stockouts.")
