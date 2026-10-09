# MacroOps AI — Master Operational Dataset Report

**Project:** MacroOps AI  
**Phase:** Phase 03 — Data Engineering & Analytics  
**Date:** October 2026  
**Output:** `data/processed/master_operational.csv`

## 1. Objective

Create an order-level operational dataset by combining order, picking and delivery information while preserving every order in the source orders table.

## 2. Source Datasets

| Dataset | Source rows |
|---|---:|
| Orders | 100,000 |
| Picking | 25,000 |
| Delivery | 25,000 |

## 3. Merge Strategy

- Used the `order_id` column as the join key.
- Used left joins, preserving all rows from the orders dataset.
- Renamed picking and delivery columns with prefixes to distinguish them from order columns.
- Applied one-to-one merge validation to prevent duplicate join keys from multiplying rows.

## 4. Validation Results

| Check | Result |
|---|---|
| Master dataset rows | 100,000 |
| Master dataset columns | 22 |
| Unique order IDs | 100,000 |
| Duplicate order IDs | 0 |
| Orders without picking records | 75,000 |
| Orders without delivery records | 75,000 |
| Total missing cells | 900,000 |

The row count and uniqueness checks passed. The 900,000 missing cells are consistent with the unmatched picking and delivery records: each absent picking or delivery record contributes seven missing columns for its order.

## 5. Interpretation and Limitations

The master dataset preserves the complete orders table. However, only 25,000 orders have matching picking records, and those same 25,000 orders have matching delivery records.

The missing operational records must not automatically be interpreted as zero-duration activity, failed operations or cancelled orders. Their absence may reflect the construction or coverage of the synthetic datasets.

The merged dataset is structurally valid for order-level analysis, but it is not yet sufficient to establish operational causes of SLA breaches. Additional validation and feature-level analysis are required.

## 6. Next Steps

1. Confirm why picking and delivery data cover only 25% of orders.
2. Validate relationships between operational timestamps and recorded duration fields.
3. Investigate workforce identifier inconsistencies.
4. Build baseline operational analytics and document their assumptions.

## 7. Status

**Completed:** Initial order-level master dataset and structural validation.  
**Pending:** Investigation of source coverage, business-rule consistency and analytical readiness.