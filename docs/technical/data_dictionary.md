# MacroOps AI — Data Dictionary

**Project:** MacroOps AI  
**Phase:** Phase 03 — Data Engineering & Analytics  
**Date:** October 2026  
**Data source:** Synthetic quick-commerce operational datasets

## 1. Dataset Overview

| Dataset | Records | Columns | Purpose |
|---|---:|---:|---|
| Orders | 100,000 | 10 | Order details, delivery status and SLA performance |
| Picking | 25,000 | 7 | Picking activity and missing items |
| Delivery | 25,000 | 7 | Rider assignment, delivery timing and distance |
| Inventory | 40,000 | 7 | Stock levels and inventory accuracy |
| Workforce | 10,000 | 6 | Employee roles, shifts and workload |
| **Total** | **200,000** | **37** | **Operational analysis across five tables** |

The datasets represent separate operational entities. The combined record count is not the number of unique orders.

## 2. Orders Dataset

| Column | Data type | Description |
|---|---|---|
| `order_id` | String | Unique order identifier |
| `store_id` | String | Store associated with the order |
| `order_time` | Datetime | Time the order was placed |
| `item_count` | Integer | Number of items in the order |
| `order_value` | Float | Monetary value of the order |
| `promised_time` | Datetime | Promised delivery time |
| `actual_delivery_time` | Datetime | Recorded actual delivery time |
| `status` | String | Order outcome or delivery status |
| `sla_breached` | Integer | SLA breach indicator (0 or 1 in this dataset) |
| `delivery_delay_minutes` | Float | Recorded delivery delay in minutes |

Observed statuses: `Delivered_Late`, `Delivered_On_Time`, `Cancelled`, and `Failed`.

## 3. Picking Dataset

| Column | Data type | Description |
|---|---|---|
| `order_id` | String | Order associated with the picking activity |
| `picker_id` | String | Identifier of the picker |
| `pick_start` | Datetime | Picking start time |
| `pick_end` | Datetime | Picking end time |
| `items_picked` | Integer | Number of items picked |
| `items_missing` | Integer | Number of missing items recorded |
| `pick_duration_minutes` | Float | Recorded picking duration in minutes |

## 4. Delivery Dataset

| Column | Data type | Description |
|---|---|---|
| `order_id` | String | Order associated with the delivery record |
| `rider_id` | String | Identifier of the delivery rider |
| `assignment_time` | Datetime | Time the delivery was assigned |
| `pickup_time` | Datetime | Time the rider picked up the order |
| `delivery_time` | Datetime | Recorded delivery completion time |
| `distance_km` | Float | Delivery distance in kilometres |
| `assignment_delay_minutes` | Float | Recorded delay before rider assignment |

## 5. Inventory Dataset

| Column | Data type | Description |
|---|---|---|
| `store_id` | String | Store associated with the stock record |
| `sku_id` | String | Stock-keeping unit identifier |
| `system_stock` | Integer | Stock quantity recorded in the system |
| `physical_stock` | Integer | Stock quantity recorded physically |
| `stockout` | String | Stockout indicator (`Yes` or `No`) |
| `stock_variance` | Integer | Difference between physical and system stock |
| `inventory_accuracy_pct` | Float | Recorded inventory accuracy percentage |

## 6. Workforce Dataset

| Column | Data type | Description |
|---|---|---|
| `employee_id` | String | Employee identifier |
| `role` | String | Employee's operational role |
| `store_id` | String | Store associated with the employee record |
| `shift` | String | Employee's shift |
| `tasks_completed` | Integer | Number of tasks completed |
| `tasks_pending` | Integer | Number of tasks pending |

Observed roles include Picker, Store Associate, Packer, Rider Coordinator and Supervisor. Observed shifts include Morning, Afternoon, Evening and Night.

## 7. Key Relationships

- `orders.order_id` → `picking.order_id`
- `orders.order_id` → `delivery.order_id`
- `orders.store_id` → `inventory.store_id`
- `orders.store_id` → `workforce.store_id`

These are candidate relationships based on matching column names. Key uniqueness, match coverage and join cardinality must be validated before combining tables.

## 8. Important Data Considerations

- The data are synthetic and should not be presented as live production measurements.
- The orders dataset contains 100,000 rows, while picking and delivery each contain 25,000 rows.
- The orders status counts and SLA indicators should be interpreted using the actual recorded values.
- Column meanings and calculated fields should be verified against the data-generation logic where available.
- Initial quality checks detected no issues using the checks implemented so far. This does not establish that all data-quality risks have been ruled out.
- Validate identifiers, join coverage, timestamp consistency, metric formulas and business rules before feature engineering or model training.

## 9. Status

**Completed:** Initial dataset inspection and data dictionary draft.  
**Next:** Validate primary keys, foreign-key coverage, join cardinality and calculated metrics.