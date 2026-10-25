
import streamlit as st
import pandas as pd
import plotly.express as px

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


# --------------------------------------------------
# Load exception data
# --------------------------------------------------

@st.cache_data
def load_exceptions():
    return detect_exceptions(limit=100000)


exceptions = load_exceptions()

if exceptions.empty:
    st.success("No exceptions detected in the current dataset.")
    st.stop()


# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------

st.sidebar.header("Exception Filters")

severity_order = ["Critical", "High", "Medium", "Low"]

available_severities = [
    level
    for level in severity_order
    if level in exceptions["severity"].unique()
]

selected_severities = st.sidebar.multiselect(
    "Severity",
    options=available_severities,
    default=available_severities,
)

available_types = sorted(exceptions["exception_type"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Exception type",
    options=available_types,
    default=available_types,
)

available_stores = sorted(
    store
    for store in exceptions["store_id"].dropna().astype(str).unique()
    if store != "N/A"
)

selected_stores = st.sidebar.multiselect(
    "Store",
    options=available_stores,
    default=available_stores,
)

search_text = st.sidebar.text_input(
    "Search exceptions",
    placeholder="ID, entity, store, or description",
)


# --------------------------------------------------
# Apply filters
# --------------------------------------------------

filtered = exceptions[
    exceptions["severity"].isin(selected_severities)
    & exceptions["exception_type"].isin(selected_types)
].copy()

if selected_stores:
    filtered = filtered[
        filtered["store_id"].astype(str).isin(selected_stores)
    ]
elif available_stores:
    # No store selected means no store-specific records.
    filtered = filtered[
        ~filtered["store_id"].astype(str).isin(available_stores)
    ]

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


# --------------------------------------------------
# Summary metrics
# --------------------------------------------------

st.subheader("Exception Summary")

critical_count = (filtered["severity"] == "Critical").sum()
high_count = (filtered["severity"] == "High").sum()
medium_count = (filtered["severity"] == "Medium").sum()
open_count = (filtered["status"] == "Open").sum()

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Exceptions", f"{len(filtered):,}")
m2.metric("Critical", f"{critical_count:,}")
m3.metric("High", f"{high_count:,}")
m4.metric("Open", f"{open_count:,}")

st.divider()


# --------------------------------------------------
# Severity distribution
# --------------------------------------------------

st.subheader("Exception Analysis")

left, right = st.columns(2)

with left:
    st.markdown("**Exceptions by Severity**")

    if filtered.empty:
        st.info("No exceptions match the selected filters.")
    else:
        severity_counts = (
            filtered["severity"]
            .value_counts()
            .reindex(severity_order, fill_value=0)
            .reset_index()
        )
        severity_counts.columns = ["Severity", "Count"]
        severity_counts = severity_counts[
            severity_counts["Count"] > 0
        ]

        fig_severity = px.bar(
            severity_counts,
            x="Severity",
            y="Count",
            color="Severity",
            category_orders={"Severity": severity_order},
            title="Severity Distribution",
        )
        fig_severity.update_layout(showlegend=False)
        st.plotly_chart(fig_severity, use_container_width=True)

with right:
    st.markdown("**Exceptions by Type**")

    if filtered.empty:
        st.info("No exception types to display.")
    else:
        type_counts = (
            filtered["exception_type"]
            .value_counts()
            .rename_axis("Exception Type")
            .reset_index(name="Count")
        )

        fig_type = px.bar(
            type_counts,
            x="Count",
            y="Exception Type",
            orientation="h",
            title="Exception Type Distribution",
        )
        st.plotly_chart(fig_type, use_container_width=True)


# --------------------------------------------------
# Exception records
# --------------------------------------------------

st.divider()
st.subheader("Detected Exceptions")

if filtered.empty:
    st.info("No exceptions match the selected filters.")
else:
    display_columns = [
        "exception_id",
        "severity",
        "exception_type",
        "entity_id",
        "store_id",
        "description",
        "recommended_action",
        "status",
        "detected_at",
    ]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    csv_data = filtered[display_columns].to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download filtered exceptions as CSV",
        data=csv_data,
        file_name="macroops_exceptions.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# Detailed exception cards
# --------------------------------------------------

st.divider()
st.subheader("Exception Details")

if not filtered.empty:
    for _, row in filtered.head(20).iterrows():
        severity = row["severity"]

        with st.container(border=True):
            st.markdown(
                f"**{row['exception_id']} — "
                f"{row['exception_type']}**"
            )

            st.caption(
                f"Severity: {severity} | "
                f"Store: {row['store_id']} | "
                f"Status: {row['status']}"
            )

            st.write(row["description"])

            st.markdown("**Recommended action**")
            st.write(row["recommended_action"])

            st.caption(
                f"Entity: {row['entity_id']} | "
                f"Detected at: {row['detected_at']}"
            )

    if len(filtered) > 20:
        st.caption(
            "Showing the first 20 exception details. "
            "Use the table above to review all filtered records."
        )


st.caption(
    "Data source: MacroOps AI synthetic operational datasets. "
    "Recommended actions are system-generated guidance and should be reviewed."
)
