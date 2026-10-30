# ML Model Documentation — SLA Breach Prediction

**Author:** Shivya  
**Date:** October 23, 2026  
**Project:** MacroOps AI

## 1. Objective

Predict whether an order will breach its Service Level Agreement (SLA) after picking and rider assignment, but before delivery is completed. The task is formulated as binary classification using `sla_breached`.

## 2. Dataset

- **Source:** `data/processed/master_operational.csv`
- **Original dataset:** 100,000 orders and 22 columns.
- **Eligible modelling records:** 25,000 orders with the required picking and delivery process information.
- **SLA breach rate:** 89.72%.
- **Chronological split:**
  - Training: 17,500 (70%)
  - Validation: 2,500 (10%)
  - Test: 5,000 (20%)
- **Training period:** September 1–22, 2026.
- **Test period:** September 24–30, 2026.

Only orders with the required process fields and target information were retained.

## 3. Model Features

The model uses 11 features grouped as follows.

**Order features**
- `item_count`
- `order_value`
- `order_hour`
- `order_day`
- `is_peak_hour`
- `sla_window_minutes`

**Picking features**
- `picking_pick_duration_minutes`
- `picking_items_picked`
- `picking_items_missing`

**Dispatch and delivery features**
- `delivery_assignment_delay_minutes`
- `delivery_distance_km`

No separate store-context feature is currently included.

## 4. Leakage Controls

The prediction point is after picking and rider assignment, before delivery completion.

The following outcome-related fields are declared in the `LEAKY` list and excluded from model inputs:

- `actual_delivery_time`
- `status`
- `delivery_delay_minutes`
- `delivery_delivery_time`
- `delivery_pickup_time`

A code assertion checks that none of the declared leaky fields overlap with the selected features. The model feature list also excludes other post-outcome fields.

## 5. Models Compared

Four approaches were evaluated:

1. Majority baseline
2. Logistic Regression
3. Random Forest
4. XGBoost

Model selection was based on validation ROC-AUC. Logistic Regression achieved the highest validation ROC-AUC of **0.6148** among the trained models and was selected for final testing.

## 6. Test Results

| Model | Accuracy | ROC-AUC | PR-AUC | F1 Breach | F1 On-time | Precision | Recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| Majority baseline | 0.9000 | 0.5000 | 0.9000 | 0.9474 | 0.0000 | 0.9000 | 1.0000 |
| Logistic Regression | 0.5704 | 0.6197 | 0.9334 | 0.7033 | 0.2217 | 0.9292 | 0.5658 |
| Random Forest | 0.6146 | 0.6157 | 0.9327 | 0.7440 | 0.2208 | 0.9250 | 0.6222 |
| XGBoost | 0.9000 | 0.6040 | 0.9298 | 0.9474 | 0.0000 | 0.9000 | 1.0000 |

**Selected model:** Logistic Regression.

Although the majority baseline and XGBoost achieved 90% accuracy, they predicted all test orders as breaches at the default classification threshold. Their on-time F1-score was zero. Accuracy alone is therefore misleading for this imbalanced dataset.

## 7. PRD Target Check — FR-009

**Target:** ROC-AUC ≥ 0.80.

**Achieved test ROC-AUC:** 0.6197.

**Status: NOT MET.**

The selected model did not achieve the required ROC-AUC. This limitation is documented rather than presenting the model as meeting the PRD target.

## 8. Explainability

SHAP was used to interpret the selected model and identify influential features.

**Top three features by mean absolute SHAP value:**

| Feature | Mean absolute SHAP |
|---|---:|
| `item_count` | 0.16038 |
| `picking_items_picked` | 0.15183 |
| `sla_window_minutes` | 0.08071 |

Order complexity and picking workload are operationally plausible contributors to SLA risk. SHAP importance describes model behaviour, not proof of causation.

The implementation provides global feature-importance plots and individual order explanations with suggested operational actions.

## 9. Risk Tiers

The dashboard uses validation-derived probability cutoffs saved with the model:

- **Medium threshold:** 0.5094
- **High threshold:** 0.6219

Orders are classified into Low, Medium, and High risk categories using these cutoffs. These are probability thresholds, not relative top-20% and next-30% rankings. This approach was used instead of the fixed 0.4/0.7 cutoffs proposed in FR-007.

## 10. Limitations

- The dataset is synthetic; learned relationships may not represent real-world operations.
- Only orders with the required picking and delivery process records can be scored.
- The breach class is highly imbalanced, at 89.72%.
- The selected model's test ROC-AUC is below the FR-009 target.
- Classification metrics use the default 0.5 threshold.
- The dashboard scores held-out historical test-period orders in demonstration mode; it does not provide live predictions.
- SHAP explanations describe model contributions and should not be interpreted as causal findings.

## 11. Supporting Files

- `src/ai/feature_engineering.py`
- `src/ai/train_sla_model.py`
- `src/ai/shap_analysis.py`
- `src/ai/sla_predictor.py`
- `reports/ml_evaluation.csv`
- `reports/shap_importance_sla.csv`
- `reports/figures/11_ml_evaluation.png`
- `reports/figures/12_shap_bar.png`
- `reports/figures/13_shap_dot.png`
- `src/app/pages/page_04_sla_risk.py`