
"""
MacroOps AI — Main Streamlit Application
Author: Shivya
Date: October 2026
"""

from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent.parent

if str(PROJECT_ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="MacroOps AI",
    page_icon="🏠",
    layout="wide",
)

overview_page = st.Page(
    str(APP_DIR / "pages" / "page_01_overview.py"),
    title="Operations Overview",
    icon="🏠",
    default=True,
)

exceptions_page = st.Page(
    str(APP_DIR / "pages" / "page_02_exceptions.py"),
    title="Exception Management",
    icon="🚨",
)

inventory_page = st.Page(
    str(APP_DIR / "pages" / "3_Inventory_Status.py"),
    title="Inventory Status",
    icon="📦",
)

navigation = st.navigation(
    [
        overview_page,
        exceptions_page,
        inventory_page,
    ]
)

navigation.run()
