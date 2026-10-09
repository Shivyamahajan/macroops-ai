# Data Quality Report — MacroOps AI

**Author:** Shivya Mahajan  
**Date:** October 2026  
**Dataset:** MacroOps AI Synthetic Operational Dataset

## 1. Overview

The five synthetic operational datasets were loaded using `src/analytics/load_data.py` and checked using `src/analytics/data_quality_report.py`.

The initial checks covered missing values, duplicate rows, selected timestamp and SLA consistency conditions, invalid numeric values, and inventory variance calculations.

## 2. Dataset Summary

| Dataset | Rows | Columns | Missing Values | Duplicate Rows |
|---|---:|---:|---:|---:|
| Orders | 100,000 | 10 | 0 | 0 |
| Picking | 25,000 | 7 | 0 | 0 |
| Delivery | 25,000 | 7 | 0 | 0 |
| Inventory | 40,000 | 7 | 0 | 0 |
| Workforce | 10,000 | 6 | 0 | 0 |
| **Total records across tables** | **200,000** | **37** | **0** | **0** |

*Note: The total is the sum of records across five separate tables, not the number of unique orders.*

## 3. Initial Check Results

| Check | Result |
|---|---|
| Missing values | None detected |
| Duplicate complete rows | None detected |
| Orders delivered before order placement | None detected |
| Delivered_Late records with `sla_breached = 0` | None detected |
| Negative delivery delay values | None detected |
| Zero or negative picking duration | None detected |
| Negative picked or missing item counts | None detected |
| Negative inventory stock values | None detected |
| Inventory variance calculation mismatches | None detected |
| Negative workforce task counts | None detected |

## 4. Findings and Interpretation

The initial checks did not identify any issues in the tested conditions. All five datasets loaded successfully, and the expected row and column counts were confirmed.

However, these results do not establish that every field is semantically correct or that all table relationships are valid. Additional checks are still required for primary-key uniqueness, foreign-key coverage, category validity, join duplication, and consistency between derived metrics and source fields.

## 5. Limitations

- The datasets are synthetic and should not be treated as live production data.
- The report only covers the checks implemented in the current script.
- A clean result from these checks does not guarantee the absence of every possible data-quality issue.
- The report will be updated as additional validation checks are implemented.

## 6. Next Steps

1. Complete the data dictionary using actual CSV column names and verified values.
2. Validate primary keys and relationships between tables.
3. Build the joined master operational dataset.
4. Recheck row counts and join coverage after merging.
5. Calculate and validate the project's operational KPIs.

---

**Status:** Initial data-quality checks completed successfully; extended validation pending.
### Additional Finding: Workforce Identifier Consistency

The workforce dataset contains 10,000 records but only 2,456 unique employee IDs. Further investigation found that 2,131 of these IDs are associated with multiple roles, 2,282 with multiple stores, and 2,134 with multiple shifts.

For example, `EMP00001` appears in multiple roles and stores. Although repeated rows may represent separate observations, the variation in role and store suggests that employee IDs may not consistently identify a single employee profile.

**Impact:** Employee-level metrics, role comparisons, and store-level workforce analysis may be misleading if records are grouped by employee ID without further validation.

**Action required:** Review the synthetic data-generation logic and determine whether workforce rows represent employee profiles, shift-level observations, or other operational records. Do not deduplicate or aggregate these records until their intended grain is established.