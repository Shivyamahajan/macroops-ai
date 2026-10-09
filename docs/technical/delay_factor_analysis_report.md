# Delay Factor Analysis Report

**Project:** MacroOps AI  
**Phase:** Phase 03 — Data Foundation and Analytics  
**Dataset:** Synthetic quick-commerce operational data

## 1. Objective

Compare selected operational metrics between late and on-time deliveries to identify potential areas for further investigation.

## 2. Dataset Coverage

- Delivered orders analysed: 97,449
- Orders with picking, rider assignment, and distance data: 24,369 (25.01%)
- Orders with item-count data: 97,449 (100%)

Operational metrics have incomplete coverage and may not represent all delivered orders.

## 3. Comparison of Operational Metrics

| Metric | Delivered Late | Delivered On Time |
|---|---:|---:|
| Average picking duration | 13.18 min | 11.74 min |
| Average rider assignment delay | 8.16 min | 8.21 min |
| Average delivery distance | 3.51 km | 3.52 km |
| Average items per order | 5.08 | 4.29 |

## 4. Initial Findings

### Picking Duration

Late deliveries had an average recorded picking duration approximately 1.44 minutes longer than on-time deliveries within the available subset. This is a potential relationship to investigate further.

### Rider Assignment Delay

Average assignment delays were very similar between the two delivery groups. Further analysis is needed before concluding whether assignment delay contributes meaningfully to late delivery.

### Delivery Distance

Average delivery distances were nearly identical between the groups in the available subset. Average distance alone may not explain the observed difference in delivery status.

### Order Size

Late deliveries contained approximately 0.79 more items per order on average. Larger orders may require more picking effort, but this comparison does not establish causation.

## 5. Limitations

- Operational metrics are available for only 25.01% of delivered orders.
- The operational subset may not be representative of all orders.
- Results are based on synthetic data, not live business operations.
- These are averages; they do not show statistical significance or establish causal relationships.
- Other variables, including store workload, order time, and staffing, have not yet been controlled for.

## 6. Recommended Next Steps

1. Investigate the coverage and selection of operational records.
2. Compare item count and picking duration together.
3. Analyse SLA performance by store.
4. Explore whether workload and time of day are associated with delays.
5. Revisit the conclusions after further validation.

**Status:** Initial delay factor analysis completed.
