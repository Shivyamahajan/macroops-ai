"""
Root-Cause Insights Module — MacroOps AI

Purpose:
Analyze operational exceptions and identify likely causes
to help operations teams decide what to investigate first.

Author: Shivya
Date: October 2026
"""

from __future__ import annotations

import pandas as pd

from src.analytics.exception_engine import detect_exceptions

def explain_root_cause(exception_type: str, description: str) -> dict:
    """
    Return a likely root cause and investigation recommendation
    for an operational exception.

    These are rule-based hypotheses, not confirmed causes.
    """
    explanations = {
        "Slow Pick": {
            "likely_cause": (
                "Picker workload, inefficient item locations, "
                "or delays during order picking."
            ),
            "investigation": (
                "Review pick duration, picker workload, and "
                "item-location layout."
            ),
        },
        "Missing Items": {
            "likely_cause": (
                "Shelf stock may be unavailable, misplaced, "
                "or inconsistent with inventory records."
            ),
            "investigation": (
                "Verify physical shelf stock and review "
                "substitution records."
            ),
        },
        "High Assignment Delay": {
            "likely_cause": (
                "Limited rider availability or a backlog "
                "in the dispatch queue."
            ),
            "investigation": (
                "Compare assignment delays with rider availability "
                "and dispatch workload."
            ),
        },
        "Inventory Discrepancy": {
            "likely_cause": (
                "Physical stock may differ from the quantity "
                "recorded in the system."
            ),
            "investigation": (
                "Perform a physical count and review recent "
                "stock movements."
            ),
        },
        "Stockout": {
            "likely_cause": (
                "The item may be unavailable or its stock "
                "record may need updating."
            ),
            "investigation": (
                "Verify physical availability and check "
                "replenishment records."
            ),
        },
        "Overloaded Employee": {
            "likely_cause": (
                "Workload may be unevenly distributed "
                "across employees."
            ),
            "investigation": (
                "Review pending tasks and redistribute work "
                "if staffing allows."
            ),
        },
    }

    result = explanations.get(
        exception_type,
        {
            "likely_cause": "The cause is not yet identified.",
            "investigation": (
                "Review the exception details and relevant "
                "operational records."
            ),
        },
    ).copy()

    result["evidence"] = description
    return result


def generate_root_cause_insights(limit: int = 500) -> pd.DataFrame:
    """
    Generate root-cause insights for detected operational exceptions.

    Returns a DataFrame with the original exception details,
    likely causes, investigation recommendations, and evidence.
    """
    exceptions = detect_exceptions(limit=limit)

    if exceptions.empty:
        return exceptions.assign(
            likely_cause=pd.Series(dtype="object"),
            investigation=pd.Series(dtype="object"),
            evidence=pd.Series(dtype="object"),
        )

    insights = []

    for _, exception in exceptions.iterrows():
        explanation = explain_root_cause(
            exception_type=exception["exception_type"],
            description=exception["description"],
        )

        insights.append(
            {
                **exception.to_dict(),
                **explanation,
            }
        )

    return pd.DataFrame(insights)  