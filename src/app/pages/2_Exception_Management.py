
import streamlit as st
import pandas as pd

from src.analytics.exception_engine import detect_exceptions

st.set_page_config(
    page_title="Exception Management | MacroOps AI",
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 Exception Management")
st.caption(
    "Identify operational issues, assess severity, and review recommended actions."
)


@st.cache_data
def load_exceptions():
    return detect_exceptions(limit=100000)


exceptions = load_exceptions()

if exceptions.empty:
    st.success("No exceptions detected in the current dataset.")
    st.stop()

# Sidebar filters
st.sidebar.subheader("Exception Filters")

severity_options = ["Critical", "High", "Medium", "Low"]
available_severities = [
    severity
    for severity in severity_options
    if severity in exceptions["severity"].unique()
]

selected_severities = st.sidebar.multiselect(
    "Filter by severity",
    options=available_severities,
    default=available_severities,
)

available_types = sorted(exceptions["exception_type"].unique())

selected_types = st.sidebar.multiselect(
    "Filter by exception type",
    options=available_types,
    default=available_types,
)

search_text = st.sidebar.text_input(
    "Search by ID, store, or description"
)

filtered = exceptions[
    exceptions["severity"].isin(selected_severities)
    & exceptions["exception_type"].isin(selected_types)
].copy()

if search_text.strip():
    search_mask = (
        filtered.astype(str)
        .apply(
            lambda column: column.str.contains(
                search_text.strip(),
                case=False,
                na=False,
                regex=False,
            )
        )
        .any(axis=1)
    )
    filtered = filtered[search_mask]

# Summary metrics
st.subheader("Exception Summary")

critical_count = (filtered["severity"] == "Critical").sum()
high_count = (filtered["severity"] == "High").sum()
medium_count = (filtered["severity"] == "Medium").sum()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Filtered Exceptions", f"{len(filtered):,}")
m2.metric("Critical", f"{critical_count:,}")
m3.metric("High", f"{high_count:,}")
m4.metric("Medium", f"{medium_count:,}")

st.divider()

# Exception records
st.subheader("Detected Exceptions")

display_columns = [
    "exception_id",
    "exception_type",
    "severity",
    "entity_id",
    "store_id",
    "description",
    "recommended_action",
    "status",
]

display_columns = [
    column for column in display_columns if column in filtered.columns
]

if filtered.empty:
    st.info("No exceptions match the selected filters.")
else:
    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    csv_data = filtered[display_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download filtered exceptions as CSV",
        data=csv_data,
        file_name="macroops_filtered_exceptions.csv",
        mime="text/csv",
    )

st.caption(
    "Data source: MacroOps AI synthetic operational datasets. "
    "Recommended actions are system-generated guidance and should be reviewed."
)
