
"""
SHAP Explainability — SLA Risk Model — MacroOps AI
Author: Shivya | October 2026
"""

import sys
sys.path.insert(0, ".")

import joblib
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap

from src.analytics.load_data import load_master
from src.ai.feature_engineering import build_ml_table, time_split


def main():
    bundle = joblib.load("models/sla_model.pkl")
    model = bundle["model"]
    feats = bundle["features"]

    master = load_master()
    table, _ = build_ml_table(master)
    _, _, test = time_split(table)

    sample = test[feats].sample(
        min(2000, len(test)),
        random_state=42
    )

    # Handle the Logistic Regression pipeline
    estimator = (
        model.steps[-1][1]
        if hasattr(model, "steps")
        else model
    )

    data = (
        model.steps[0][1].transform(sample)
        if hasattr(model, "steps")
        else sample
    )

    if bundle["model_name"] == "Logistic Regression":
        explainer = shap.LinearExplainer(estimator, data)
    else:
        explainer = shap.TreeExplainer(estimator)

    shap_values = explainer.shap_values(data)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap_values = np.asarray(shap_values)

    # Handle SHAP outputs with an additional class dimension
    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, 1]

    if shap_values.shape != (len(sample), len(feats)):
        raise ValueError(
            f"Unexpected SHAP shape: {shap_values.shape}"
        )

    # Global feature importance bar chart
    plt.figure(figsize=(10, 7))
    shap.summary_plot(
        shap_values,
        sample,
        plot_type="bar",
        show=False
    )
    plt.title("SHAP Feature Importance — SLA Breach Model")
    plt.tight_layout()
    plt.savefig(
        "reports/figures/12_shap_bar.png",
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()

    # SHAP summary dot chart
    plt.figure(figsize=(10, 7))
    shap.summary_plot(
        shap_values,
        sample,
        show=False
    )
    plt.tight_layout()
    plt.savefig(
        "reports/figures/13_shap_dot.png",
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()

    # Export numerical feature importance
    importance = (
        pd.DataFrame({
            "feature": feats,
            "mean_abs_shap": np.abs(shap_values).mean(axis=0)
        })
        .sort_values("mean_abs_shap", ascending=False)
    )

    importance.to_csv(
        "reports/shap_importance_sla.csv",
        index=False
    )

    print("\nTop 10 SHAP features:")
    print(importance.head(10).to_string(index=False))

    print("\nSaved:")
    print("reports/figures/12_shap_bar.png")
    print("reports/figures/13_shap_dot.png")
    print("reports/shap_importance_sla.csv")


if __name__ == "__main__":
    main()
