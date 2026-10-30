"""
Train and Evaluate SLA Breach Prediction Models — MacroOps AI
Author: Shivya | October 2026
"""

import sys, os, joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.append('.')

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    roc_auc_score, average_precision_score, f1_score,
    precision_score, recall_score, accuracy_score,
    confusion_matrix, roc_curve, classification_report,
)
from xgboost import XGBClassifier

from src.analytics.load_data import load_master
from src.ai.feature_engineering import (
    build_ml_table, time_split, TARGET
)

RANDOM_STATE = 42


def evaluate(name, model, X, y, split):
    proba = model.predict_proba(X)[:, 1]
    pred  = (proba >= 0.5).astype(int)
    return {
        'Model': name, 'Split': split,
        'Accuracy':  round(accuracy_score(y, pred), 4),
        'ROC_AUC':   round(roc_auc_score(y, proba), 4),
        'PR_AUC':    round(average_precision_score(y, proba), 4),
        'F1_breach': round(f1_score(y, pred), 4),
        'F1_ontime': round(f1_score(y, pred, pos_label=0), 4),
        'Precision': round(precision_score(y, pred, zero_division=0), 4),
        'Recall':    round(recall_score(y, pred), 4),
    }


def main():
    master = load_master()
    table, feats = build_ml_table(master)
    train, val, test = time_split(table)

    Xtr, ytr = train[feats], train[TARGET]
    Xva, yva = val[feats],   val[TARGET]
    Xte, yte = test[feats],  test[TARGET]

    models = {
        'Majority baseline': DummyClassifier(strategy='prior'),
        'Logistic Regression': make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, class_weight='balanced')),
        'Random Forest': RandomForestClassifier(
            n_estimators=200, max_depth=10, min_samples_leaf=20,
            class_weight='balanced', n_jobs=-1,
            random_state=RANDOM_STATE),
        'XGBoost': XGBClassifier(
            n_estimators=300, learning_rate=0.05, max_depth=4,
            subsample=0.8, colsample_bytree=0.8,
            eval_metric='logloss', n_jobs=-1,
            random_state=RANDOM_STATE),
    }

    results = []
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(Xtr, ytr)
        results.append(evaluate(name, model, Xtr, ytr, 'Train'))
        results.append(evaluate(name, model, Xva, yva, 'Validation'))

    res = pd.DataFrame(results)

    # ── Select best on VALIDATION ROC-AUC (exclude baseline) ──
    val_res = res[(res['Split'] == 'Validation') &
                  (res['Model'] != 'Majority baseline')]
    best_name = val_res.sort_values('ROC_AUC',
                                    ascending=False).iloc[0]['Model']
    best = models[best_name]
    print(f"\nBest model on validation: {best_name}")

    # ── Test evaluation: done once, for all models, for reporting ──
    for name, model in models.items():
        res = pd.concat([res, pd.DataFrame(
            [evaluate(name, model, Xte, yte, 'Test')])],
            ignore_index=True)

    os.makedirs('reports', exist_ok=True)
    res.to_csv('reports/ml_evaluation.csv', index=False)
    print("\n=== TEST SET RESULTS ===")
    print(res[res['Split'] == 'Test'].to_string(index=False))

    test_auc = res[(res['Split']=='Test') &
                   (res['Model']==best_name)]['ROC_AUC'].iloc[0]
    print(f"\nPRD target (FR-009): ROC-AUC >= 0.80 | "
          f"achieved: {test_auc:.4f} | "
          f"{'MET' if test_auc >= 0.80 else 'NOT MET — report honestly'}")

    # ── Risk tier cutoffs from VALIDATION probabilities ──
    # With ~90% base rate, fixed cutoffs (0.4/0.7) would label almost
    # everything High. Use relative ranking instead.
    pv = best.predict_proba(Xva)[:, 1]
    cutoffs = {'high': float(np.quantile(pv, 0.80)),
               'medium': float(np.quantile(pv, 0.50))}

    # ── Save bundle ──
    os.makedirs('models', exist_ok=True)
    joblib.dump({
        'model': best, 'model_name': best_name, 'features': feats,
        'cutoffs': cutoffs,
        'test_start': str(test['order_time'].min()),
    }, 'models/sla_model.pkl')
    print("Saved models/sla_model.pkl")

    # ── Charts ──
    os.makedirs('reports/figures', exist_ok=True)
    proba = best.predict_proba(Xte)[:, 1]

    fig, ax = plt.subplots(1, 3, figsize=(17, 5))
    fpr, tpr, _ = roc_curve(yte, proba)
    ax[0].plot(fpr, tpr, label=f'{best_name} (AUC={test_auc:.3f})')
    ax[0].plot([0, 1], [0, 1], 'k--', label='Random')
    ax[0].set(title='ROC Curve (Test)', xlabel='False Positive Rate',
              ylabel='True Positive Rate')
    ax[0].legend()

    cm = confusion_matrix(yte, (proba >= 0.5).astype(int))
    ax[1].imshow(cm, cmap='Blues')
    ax[1].set(title='Confusion Matrix (Test, threshold 0.5)',
              xticks=[0, 1], yticks=[0, 1],
              xticklabels=['On time', 'Breach'],
              yticklabels=['On time', 'Breach'],
              xlabel='Predicted', ylabel='Actual')
    for (i, j), v in np.ndenumerate(cm):
        ax[1].text(j, i, f'{v:,}', ha='center', va='center',
                   color='red', fontsize=12)

    ax[2].hist(proba[yte == 1], bins=40, alpha=0.6,
               label='Actual breach')
    ax[2].hist(proba[yte == 0], bins=40, alpha=0.6,
               label='Actual on-time')
    ax[2].set(title='Predicted Probability by Actual Outcome',
              xlabel='P(breach)')
    ax[2].legend()
    plt.tight_layout()
    plt.savefig('reports/figures/11_ml_evaluation.png',
                dpi=150, bbox_inches='tight')
    plt.close()

    print("\nClassification report (test, threshold 0.5):")
    print(classification_report(
        yte, (proba >= 0.5).astype(int),
        target_names=['On time', 'Breach']))


if __name__ == "__main__":
    main()