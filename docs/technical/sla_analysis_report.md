# SLA Performance Analysis Report

**Project:** MacroOps AI  
**Phase:** Phase 03 — Data Foundation and Analytics  
**Dataset:** Synthetic quick-commerce operational data

## 1. Objective

Analyse order statuses, recorded SLA breaches, delivery delays, and delay distribution to establish an initial operational performance baseline.

## 2. Dataset Overview

- Total order records: 100,000
- Delivered late: 87,392 (87.39%)
- Delivered on time: 10,057 (10.06%)
- Cancelled: 1,795 (1.80%)
- Failed: 756 (0.76%)

## 3. Overall SLA Results

- Records flagged as SLA breached: 89,674
- SLA breach-flag rate across all records: 89.67%
- Average recorded delivery delay: 6.43 minutes
- Median recorded delay: 5.80 minutes
- Maximum recorded delay: 37.30 minutes

The 89.67% figure includes cancelled and failed records. It should not be interpreted as the breach rate among completed deliveries alone.

## 4. Delivered-Order SLA Performance

Among the 97,449 records labelled as delivered:

- Delivered late: 87,392
- Delivered on time: 10,057
- Late-delivery rate among delivered records: approximately 89.68%

The status labels and SLA flags are consistent in this dataset: every record labelled `Delivered_Late` is flagged as breached, while every record labelled `Delivered_On_Time` is not.

## 5. Delay Distribution

- Zero recorded delay: 10,592 records (10.59%)
- Above 0 to 5 minutes: 33,979 records (33.98%)
- Above 5 to 10 minutes: 33,478 records (33.48%)
- Above 10 to 15 minutes: 15,890 records (15.89%)
- Above 15 minutes: 6,061 records (6.06%)

These delay bands were calculated across all order records, including cancelled and failed records.

## 6. Initial Interpretation

The synthetic dataset contains a high proportion of records marked as late. Delay analysis can help identify patterns for further investigation, such as picking duration, rider assignment delay, store-level variation, and delivery distance.

These figures describe the generated dataset and are not evidence of actual quick-commerce business performance.

## 7. Limitations and Next Steps

- Validate how SLA flags and statuses were generated.
- Analyse SLA performance by store and time period.
- Compare picking and rider assignment delays with delivery outcomes.
- Use only appropriate records and clearly defined metrics for each analysis.
- Investigate whether synthetic data generation creates unrealistic patterns.

**Status:** Initial SLA analysis completed.
