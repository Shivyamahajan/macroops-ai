
"""
SLA Predictor — scoring + per-order explanations — MacroOps AI
Author: Shivya | October 2026
"""

import sys
sys.path.insert(0, ".")

import joblib
import numpy as np
import pandas as pd
import shap


LABELS = {
    "picking_pick_duration_minutes": ("Picking time", "min"),
    "delivery_assignment_delay_minutes": ("Rider assignment delay", "min"),
    "delivery_distance_km": ("Delivery distance", "km"),
    "picking_items_missing": ("Missing items", ""),
    "picking_items_picked": ("Items picked", ""),
    "item_count": ("Items in order", ""),
    "order_value": ("Order value", "₹"),
    "order_hour": ("Order hour", "h"),
    "order_day": ("Day of week", ""),
    "is_peak_hour": ("Peak-hour order", ""),
    "sla_window_minutes": ("SLA window", "min"),
}

ACTIONS = {
    "picking_pick_duration_minutes":
        "Check shelf locations or consider adding another picker.",
    "delivery_assignment_delay_minutes":
        "Reallocate a nearby available rider.",
    "delivery_distance_km":
        "Review dispatch priority for this longer-distance order.",
    "picking_items_missing":
        "Confirm substitutions with the customer promptly.",
    "item_count":
        "Review picking workload and staffing for this order.",
    "picking_items_picked":
        "Check picking workload and order complexity.",
}


class SLAPredictor:

    def __init__(self, path="models/sla_model.pkl"):
        bundle = joblib.load(path)

        self.model = bundle["model"]
        self.features = bundle["features"]
        self.cutoffs = bundle["cutoffs"]
        self.name = bundle["model_name"]
        self.test_start = pd.Timestamp(bundle["test_start"])

        self._is_pipeline = hasattr(self.model, "steps")

        self._estimator = (
            self.model.steps[-1][1]
            if self._is_pipeline
            else self.model
        )

        self._background = None
        self._explainer = None

    def _transform(self, X):
        if self._is_pipeline:
            return self.model.steps[0][1].transform(X)

        return X

    def _get_explainer(self, background):
        if self._explainer is None:
            transformed_background = self._transform(background)

            if self.name == "Logistic Regression":
                self._explainer = shap.LinearExplainer(
                    self._estimator,
                    transformed_background
                )
            else:
                self._explainer = shap.TreeExplainer(
                    self._estimator
                )

        return self._explainer

    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()

        probabilities = self.model.predict_proba(
            out[self.features]
        )[:, 1]

        out["risk_probability"] = probabilities

        out["risk_tier"] = np.where(
            probabilities >= self.cutoffs["high"],
            "High",
            np.where(
                probabilities >= self.cutoffs["medium"],
                "Medium",
                "Low"
            )
        )

        return out

    def explain(
        self,
        row: pd.DataFrame,
        background: pd.DataFrame,
        top_n: int = 3
    ):
        """
        Explain one order using a representative background dataset.
        Both inputs must contain the trained model's feature columns.
        """

        if len(row) != 1:
            raise ValueError("Please provide exactly one order.")

        if background.empty:
            raise ValueError("Background dataset cannot be empty.")

        X = row[self.features]
        bg = background[self.features]

        explainer = self._get_explainer(bg)

        transformed_row = self._transform(X)
        shap_values = explainer.shap_values(transformed_row)

        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        shap_values = np.asarray(shap_values)

        if shap_values.ndim == 3:
            shap_values = shap_values[:, :, 1]

        values = shap_values[0]

        order = np.argsort(-np.abs(values))[:top_n]

        results = []

        for i in order:
            feature = self.features[i]
            value = float(X.iloc[0][feature])

            label, unit = LABELS.get(
                feature,
                (feature, "")
            )

            direction = (
                "raises"
                if values[i] > 0
                else "lowers"
            )

            results.append({
                "feature": feature,
                "text": (
                    f"{label} = {value:.1f} {unit} "
                    f"{direction} breach risk"
                ),
                "shap": float(values[i]),
                "action": (
                    ACTIONS.get(feature)
                    if values[i] > 0
                    else None
                )
            })

        return results
