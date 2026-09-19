# Business Problem Statement — MacroOps AI

**Author:** Shivya
**Date:** September 17, 2026

---

## Executive Summary

Quick-commerce operations in India operate under highly time-sensitive delivery commitments, with some services promising delivery within approximately 10 to 30 minutes. Store managers and operations teams need timely visibility into fulfillment performance so they can identify, understand, and respond to operational problems before they affect customers.

MacroOps AI is designed to address this operational intelligence gap by combining real-time monitoring, machine learning, and generative AI. The platform is intended to detect operational exceptions, predict orders at risk of SLA breaches, explain contributing factors, and provide actionable recommendations to operations teams.

---

## The Business Context

### Industry Scale

The Indian quick-commerce sector processes large volumes of orders through distributed networks of dark stores and fulfillment centers. Delivery speed is an important part of the customer proposition, making efficient coordination across inventory, picking, packing, rider assignment, and delivery essential to operations.

### The Operational Challenge

Quick-commerce fulfillment is complex, time-sensitive, and highly interdependent. A short delivery SLA means that order receipt, inventory availability, picking, packing, rider assignment, and delivery must be coordinated within a limited time window.

A delay at one stage reduces the time available for subsequent stages and can increase the probability of an SLA breach.

### Current State

Based on the operational scenario defined for MacroOps AI, teams may rely on:

* Multiple operational dashboards and systems
* Manual exception identification by store managers
* Periodic performance reporting
* Phone or messaging-based escalation
* Spreadsheets for additional analysis

This creates a reactive operating environment in which managers may spend significant time identifying problems instead of acting on them.

---

## The Core Problem

**A fulfillment center processing thousands of orders per day needs a way to identify, in real time, which orders are at risk of missing their promised delivery time, understand the operational factors contributing to that risk, and determine what action should be taken.**

The MacroOps AI synthetic dataset demonstrates several operational areas that motivate this problem:

1. **89.7%** of orders in the dataset have an SLA breach flag.
2. Average picking time is **13.03 minutes**, with a maximum of **33.8 minutes**.
3. Average rider assignment delay is **8.17 minutes**, with a maximum of **21.6 minutes**.
4. Average inventory accuracy is **89.4%**, with **23.3%** of inventory records below 80% accuracy.
5. Exception identification is modeled as a manual and reactive process in the current-state scenario.
6. Operational questions may require multiple manual steps across systems and spreadsheets.
7. Workforce workload varies across employees, with up to **17 pending tasks** recorded for an employee.

These findings are documented in the MacroOps AI Pain Point Analysis.

---

## Who Is Affected

### Primary Users

| Role                        | How They Are Affected                                                         |
| --------------------------- | ----------------------------------------------------------------------------- |
| Operations Manager          | Needs visibility across multiple operational problems and timely alerts       |
| Fulfillment Manager         | Needs visibility into picking and fulfillment bottlenecks                     |
| Delivery Operations Manager | Needs visibility into rider assignment delays and availability                |
| Regional Manager            | Needs a consolidated view for comparing operational performance across stores |

### Secondary Impact

* **Customers:** May receive orders late or with missing items.
* **Business:** Operational failures can contribute to refunds, customer dissatisfaction, and potential revenue loss.
* **Riders and Pickers:** Workload and performance may be affected by upstream operational problems and workload imbalances.

---

## The Desired Future State

After deploying MacroOps AI, operations teams should be able to:

1. **See everything** — Access key operational KPIs through one unified dashboard.
2. **Know before it happens** — Identify orders that are predicted to be at risk of SLA breach early enough to allow intervention.
3. **Understand why** — View the operational factors contributing to an exception or prediction.
4. **Act immediately** — Receive suggested actions associated with detected operational problems.
5. **Ask in plain language** — Query operational data using natural language and receive data-backed answers quickly.

---

## Definition of Success

MacroOps AI will be evaluated against measurable operational and usability objectives.

| Metric                    | Current State                                          | Target State                                                    |
| ------------------------- | ------------------------------------------------------ | --------------------------------------------------------------- |
| SLA Breach Detection      | Problem may be identified after or close to breach     | Identify high-risk orders sufficiently before expected breach   |
| Exception Resolution Time | Manual investigation may take significant time         | Reduce investigation and response time with AI assistance       |
| Manager Dashboard Checks  | Information may be distributed across multiple systems | Consolidated operational view                                   |
| Operational Query Time    | 15–20 minutes in the defined manual scenario           | Under 10 seconds through the Copilot                            |
| SLA Breach Rate           | 89.7% in the synthetic dataset                         | Measure and demonstrate reduction through controlled evaluation |

**Note:** The target states above are product objectives. They are not claims that the current prototype has already achieved these results. Actual improvement should be measured during testing and evaluation.

---

## Scope of MacroOps AI

### In Scope

* Real-time operations monitoring dashboard
* ML-powered SLA breach prediction
* Automated exception detection and management
* AI Operations Copilot for natural-language queries
* RAG-based SOP Assistant for frontline staff
* Business impact measurement and reporting

### Out of Scope

* Integration with live production systems
* Voice interaction
* Multilingual interface
* Rider navigation and routing systems
* Customer-facing features

The initial implementation is intended as a demonstration and research environment rather than a live production deployment.

---

## Conclusion

MacroOps AI addresses an operational intelligence gap in quick-commerce fulfillment: the need to identify emerging operational problems, understand their contributing factors, and support timely decision-making.

The synthetic dataset demonstrates measurable challenges across SLA performance, picking, rider assignment, inventory accuracy, and workforce workload. MacroOps AI is designed to bring these operational signals together through analytics, machine learning, automated exception detection, and generative AI.

The intended transformation is from a reactive operating process toward a more proactive and data-driven approach in which operations teams can detect risks earlier, investigate causes faster, and make informed operational decisions.
