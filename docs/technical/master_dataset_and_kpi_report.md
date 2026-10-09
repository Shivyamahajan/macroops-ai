# Master Dataset and KPI Analysis Report

**Project:** MacroOps AI  
**Phase:** Phase 03 — Business Discovery and Product Strategy  
**Task:** Day 2 — Master Dataset and KPI Calculator  
**Data source:** Synthetic quick-commerce operational datasets

## 1. Objective

The objective was to combine five operational datasets into a master dataset and develop a reusable KPI calculator for monitoring order fulfillment, delivery, inventory, and workforce operations.

## 2. Source Datasets

| Dataset | Records | Columns |
|---|---:|---:|
| Orders | 100,000 | 10 |
| Picking | 25,000 | 7 |
| Delivery | 25,000 | 7 |
| Inventory | 40,000 | 7 |
| Workforce | 10,000 | 6 |
| **Total** | **200,000** | **37** |

## 3. Master Dataset

The five datasets were integrated using order-level joins and store-level aggregations.

- Output file: `data/processed/master_operational_all_tables.csv`
- Rows: 100,000
- Columns: 49
- Unique order IDs: 100,000
- Duplicate order IDs: 0
- Missing cells: 1,125,000

The missing picking and delivery features are expected because these datasets cover only a subset of orders. Inventory and workforce features represent store-level summaries repeated across orders; they must not be summed as if they were independent order-level records.

## 4. KPI Results

| KPI | Result | Status |
|---|---:|---|
| Total orders | 100,000 | Informational |
| Delivered orders | 97,449 | Informational |
| SLA breach rate among delivered orders | 89.68% | Critical |
| On-time delivery rate among delivered orders | 10.32% | Critical |
| Average delay among late-delivered orders | 7.17 minutes | Warning |
| Average picking duration | 13.03 minutes | Warning |
| Average assignment delay | 8.17 minutes | Warning |
| Missing-item order rate in picking records | 11.68% | Critical |
| Inventory accuracy | 89.42% | Warning |
| Stockout rate | 0.01% | Good |
| High stock-variance rate | 27.43% | Critical |
| Task completion rate | 88.93% | Warning |
| Cancellation rate | 1.80% | Good |

**Note:** KPI statuses are based on configurable example thresholds in the calculator, not official industry benchmarks.

## 5. Interpretation

The synthetic data shows a high proportion of late deliveries and a low on-time delivery rate. The picking records also show missing-item issues, while inventory records indicate that stock discrepancies may warrant investigation.

The low stockout rate alongside a substantially higher stock-variance rate suggests that inventory discrepancies and stockout events should be tracked as separate measures.

Picking and delivery KPIs are based on 25,000 available records, whereas order KPIs use the 100,000-order dataset or the delivered subset. These different coverage levels must be considered when comparing metrics.

## 6. Limitations

- The data is synthetic and does not represent live business operations.
- Picking and delivery data are available for only a subset of orders.
- Store-level inventory and workforce summaries are repeated across order rows in the master dataset.
- Workforce employee identifiers may not represent consistent unique employee profiles.
- KPI statuses depend on configurable thresholds and should be reviewed before operational use.

## 7. Deliverables

- `src/analytics/create_master_dataset.py`
- `src/analytics/kpi_calculator.py`
- `data/processed/master_operational_all_tables.csv`

The scripts provide a reusable foundation for future operational dashboards, SLA monitoring, and predictive analytics.