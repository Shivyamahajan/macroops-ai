# AS-IS Process Map — Current Order Fulfillment Operations

**Project:** MacroOps AI  
**Phase:** Phase 03 — Business Discovery & Product Strategy  
**Document:** AS-IS Process Map  
**Date:** September 15, 2026

---

## 1. Overview

The AS-IS process map represents the current order fulfillment workflow before introducing AI-based improvements.

It shows how an order moves through different operational teams and systems, starting from customer order placement and ending with successful delivery.

The process involves the following roles and systems:

1. Customer — Order Placement
2. Order Management System (OMS)
3. Inventory System
4. Picker / Warehouse Staff
5. Packing & Quality Check
6. Delivery Coordinator
7. Rider
8. Customer — Delivery

---

## 2. AS-IS Process Map

![AS-IS Process Map](../../reports/figures/as_is_process_map.png)

---

## 3. Step-by-Step Process Description

### Step 1 — Customer Places Order

The customer opens the application, selects the required items, enters the delivery address, and places the order by making the required payment.

The customer then receives an order confirmation.

---

### Step 2 — Order Management System Processes Order

The OMS receives the order and validates the payment.

It then checks item availability and determines whether the requested items can be fulfilled.

If the items are available, the order is routed to the nearest suitable dark store. The OMS assigns an order ID and starts the SLA timer.

If an item is unavailable, the customer is notified and may be offered a substitute.

---

### Step 3 — Inventory Verification

The inventory system checks the stock level for each SKU in the order.

Available items are confirmed and reserved for the order. The system stock count is then updated.

This information supports the OMS in determining whether the order can proceed.

---

### Step 4 — Picking

The picker or warehouse staff receives the picking task.

The picker goes to the required shelf locations, picks the ordered items, and scans them.

If an item is found, picking continues. If an item is missing, the missing item is reported.

Once the picking activity is completed, the order is marked as picking complete.

---

### Step 5 — Packing and Quality Check

The picked items are received by the packing and quality-check team.

The team verifies the item count and condition.

If the order passes the quality check, the items are packed into the delivery bag, the order label is attached, and the order is marked ready for pickup.

If the order does not pass the quality check, it is repacked or corrected before proceeding.

---

### Step 6 — Rider Assignment

The delivery coordinator sees that the order is ready for pickup and checks the availability of riders.

If a rider is available, the nearest suitable rider is assigned and rider acceptance is monitored.

If no rider is available, the order waits or is escalated for further action.

---

### Step 7 — Delivery

The rider receives the delivery notification and travels to the dark store.

The rider picks up the packed order and navigates to the customer's address.

The order is delivered to the customer, and the rider marks the delivery as complete.

---

### Step 8 — Customer Receives Order

The customer receives the delivery and confirms receipt through the application.

The SLA timer stops after the delivery process is completed.

---

## 4. Key Decision Points

The current process contains several important decision points:

### 4.1 Item Availability

**Question:** Are the requested items available?

- **Yes:** Continue order fulfillment.
- **No:** Notify the customer and offer a substitute.

### 4.2 Item Found During Picking

**Question:** Can the picker find the required item?

- **Yes:** Continue picking.
- **No:** Report the missing item.

### 4.3 Quality Check

**Question:** Is the order correct and in acceptable condition?

- **Yes:** Pack and release the order for pickup.
- **No:** Repack or correct the order.

### 4.4 Rider Availability

**Question:** Is a suitable rider available?

- **Yes:** Assign the rider.
- **No:** Wait or escalate.

---

## 5. Data Generated During the Process

| Process Stage | Example Data Generated |
|---|---|
| Order Placement | Order ID, customer details, delivery address, payment status |
| OMS Processing | Order status, SLA start time, store assignment |
| Inventory | SKU availability, reserved quantity, stock count |
| Picking | Picking task, scan records, missing-item information |
| Packing & QC | Item verification status, quality-check status |
| Rider Assignment | Rider availability, assignment details, acceptance status |
| Delivery | Pickup time, delivery time, delivery status |
| Order Completion | Customer confirmation, SLA completion time |

---

## 6. Current Operational Pain Points Observed

The AS-IS process highlights several areas where operational challenges may occur:

- Inventory mismatches can result in unavailable or missing items.
- Picking may take different amounts of time depending on item location and workload.
- Missing items may require manual intervention.
- Quality verification and repacking can add processing time.
- Rider availability can affect order dispatch.
- Rider assignment may introduce delays during periods of high demand.
- Multiple handoffs occur between systems and operational teams.
- Real-time visibility across the complete fulfillment process may be limited.
- Delays at one stage can affect the overall order SLA.

These observations will be used as inputs for the subsequent pain-point analysis and future-state improvement discussions.

---

## 7. Summary

The AS-IS process demonstrates a multi-stage order fulfillment workflow involving the customer, OMS, inventory system, warehouse staff, packing and quality teams, delivery coordination, and riders.

The process depends on coordination between multiple systems and operational roles. This creates several opportunities to improve visibility, reduce delays, identify operational issues earlier, and support better decision-making through data, analytics, and AI.