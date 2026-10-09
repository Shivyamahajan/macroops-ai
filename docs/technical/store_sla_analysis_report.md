# Store-Level SLA Analysis Report

**Project:** MacroOps AI  
**Phase:** Phase 03 — Data Foundation and Analytics  
**Dataset:** Synthetic quick-commerce operational data

## 1. Objective

Compare late-delivery rates and recorded delivery delays across stores to identify locations that may warrant further investigation.

## 2. Key Results

- Stores analysed: 100
- Average of the individual store late-delivery rates: 89.69%
- Highest late-delivery rate: ST012 — 93.10%
- Lowest late-delivery rate: ST050 — 86.34%
- Difference between the highest and lowest rates: 6.76 percentage points

The store-level rate is calculated as late deliveries divided by the sum of late and on-time deliveries. Cancelled and failed orders are excluded from this denominator.

## 3. Stores with the Highest Late-Delivery Rates

| Store | Total Orders | Late Deliveries | On-Time Deliveries | Late-Delivery Rate |
|---|---:|---:|---:|---:|
| ST012 | 985 | 890 | 66 | 93.10% |
| ST042 | 972 | 875 | 69 | 92.69% |
| ST080 | 977 | 884 | 72 | 92.47% |
| ST024 | 989 | 892 | 73 | 92.44% |
| ST045 | 989 | 883 | 74 | 92.27% |

## 4. Stores with the Lowest Late-Delivery Rates

| Store | Total Orders | Late Deliveries | On-Time Deliveries | Late-Delivery Rate |
|---|---:|---:|---:|---:|
| ST063 | 999 | 859 | 118 | 87.92% |
| ST070 | 978 | 841 | 116 | 87.88% |
| ST035 | 972 | 826 | 114 | 87.87% |
| ST043 | 993 | 848 | 118 | 87.78% |
| ST081 | 1,034 | 888 | 125 | 87.66% |

## 5. Initial Interpretation

The late-delivery rate varies across stores. ST012 has the highest rate in this analysis, while ST050 has the lowest.

These differences can help prioritise further investigation, but they do not establish why a store has a higher or lower rate. Order timing, order size, staffing, picking duration, and delivery conditions should be examined before recommending operational changes.

The average of individual store rates is not necessarily identical to the overall order-weighted late-delivery rate.

## 6. Limitations

- Data is synthetic and does not represent live store performance.
- Store-level averages do not explain the causes of late delivery.
- Further analysis should compare operational factors and account for differences in order volume and order mix.

## 7. Recommended Next Steps

1. Compare store-level picking and rider assignment metrics where records are available.
2. Investigate whether store-level differences persist across time periods.
3. Identify possible operational factors before proposing interventions.

**Status:** Initial store-level SLA analysis completed.
