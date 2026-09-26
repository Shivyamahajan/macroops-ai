# Product Requirements Document (PRD) — MacroOps AI

**Author:** Shivya
**Date:** September 23–24, 2026
**Version:** 1.0
**Status:** Draft

---

## 1. Document Purpose

This Product Requirements Document (PRD) defines the functional and non-functional requirements for MacroOps AI v1.0. It serves as the primary reference for development work during Month 2 (October 2026) and Month 3 (November 2026).

Every feature built for the MVP should trace back to a requirement in this document.

---

## 2. Product Overview

MacroOps AI is an intelligent operations management platform for quick-commerce fulfillment operations. It combines operational analytics, machine learning, and generative AI to provide proactive operational intelligence to Operations Managers, Fulfillment Managers, Delivery Operations Managers, and frontline operational users.

**Version:** 1.0 (MVP)
**Target Release:** November 30, 2026

The MVP is intended as a demonstration system using synthetic operational data rather than live production-system integration.

---

## 3. User Stories

User stories are written in the format:

**As a [user type], I want to [do something] so that [benefit].**

### 3.1 Operations Manager User Stories

**US-001**

As an Operations Manager, I want to see all key operational KPIs on a single dashboard so that I can understand store performance without opening multiple systems.

**Acceptance Criteria:**

* Dashboard loads within the defined performance target.
* Shows a minimum of 7 core KPIs: total orders, SLA breach rate, active orders, active exceptions, average pick duration, average assignment delay, and inventory accuracy.
* Dashboard data can be refreshed automatically without requiring a manual page reload.
* Dashboard is designed to be usable on desktop and mobile browsers.

**US-002**

As an Operations Manager, I want to receive an alert when an order is predicted to breach its SLA so that I can take corrective action before the breach occurs.

**Acceptance Criteria:**

* MVP alerting target is to provide an appropriate early-warning window before the predicted breach.
* Alert includes order ID, store ID, current status, predicted breach time, and top 3 risk factors.
* Alert is visible on the dashboard exceptions view.
* Each high-risk alert includes a recommended action or next step where sufficient context is available.

**US-003**

As an Operations Manager, I want to ask the AI Copilot operational questions in plain language so that I can get data-backed answers without manually querying the underlying data.

**Acceptance Criteria:**

* Standard operational queries should meet the defined response-time target.
* Responses include specific values derived from the available operational data where applicable.
* MVP evaluation target is at least 90% correct responses on the predefined test set.
* Copilot acknowledges when the available data is insufficient rather than fabricating an answer.

**US-004**

As an Operations Manager, I want to see a list of active exceptions with severity levels so that I know which problems require attention first.

**Acceptance Criteria:**

* Exception list shows type, related ID, severity (High/Medium/Low), time raised, and current status.
* Exceptions can be sorted or displayed with higher-severity exceptions first.
* Authorized users can mark exceptions as Resolved and provide a resolution note.
* Resolved exceptions are available in a history view.

**US-005**

As an Operations Manager, I want to compare performance across different stores so that I can identify locations that require additional attention.

**Acceptance Criteria:**

* Multi-store comparison view is available.
* Metrics include SLA breach rate, average pick duration, average assignment delay, and inventory accuracy.
* Visual comparison makes differences between stores easy to identify.

---

### 3.2 Fulfillment Manager User Stories

**US-006**

As a Fulfillment Manager, I want to see picker performance metrics so that I can identify slow picking activity before it contributes to SLA breaches.

**Acceptance Criteria:**

* Dashboard shows pick duration per picker for the available shift data.
* Slow picks above the defined operational threshold are highlighted.
* Drill-down is available to inspect the individual picker's related orders where data permits.
* Dashboard data supports periodic refresh during the active session.

**US-007**

As a Fulfillment Manager, I want to see which SKUs have inventory discrepancies so that I can address stock issues before pickers waste time searching for missing items.

**Acceptance Criteria:**

* Inventory view identifies SKUs below the defined accuracy threshold.
* Records can be sorted by discrepancy severity.
* View shows system stock, physical stock, and variance where available.
* Stockout items are clearly highlighted.

**US-008**

As a Fulfillment Manager, I want to understand why an order is experiencing a delay so that I can take an appropriate corrective action.

**Acceptance Criteria:**

* Root-cause information is available for supported at-risk orders.
* Explanation can incorporate model-derived feature importance such as SHAP values and relevant operational context.
* Explanation is presented in plain operational language rather than technical terminology.
* Explanation includes a recommended action where sufficient information is available.

---

### 3.3 Delivery Operations Manager User Stories

**US-009**

As a Delivery Operations Manager, I want to monitor rider assignment delays by store so that I can identify locations where rider availability may become a problem.

**Acceptance Criteria:**

* Store-level view of assignment delays is available.
* Threshold-based alerts can be configured for elevated assignment delays.
* Time-series visualization shows assignment-delay trends where sufficient time-series data is available.
* Rider availability information is displayed where the dataset supports it.

**US-010**

As a Delivery Operations Manager, I want to receive a predictive alert when a rider shortage is likely so that I can consider operational interventions before the shortage affects SLA performance.

**Acceptance Criteria:**

* MVP should demonstrate an appropriate predictive warning window based on available data and model evaluation.
* Alert includes the projected gap between rider supply and operational demand where calculable.
* System can identify nearby stores that may have available rider capacity where the required data is available.
* Alert is clearly identified as a prediction rather than a confirmed shortage.

---

### 3.4 Frontline Picker User Stories

**US-011**

As a Frontline Picker, I want to ask the SOP Assistant questions about procedures so that I can get guidance without interrupting my supervisor.

**Acceptance Criteria:**

* SOP Assistant is accessible through a mobile-friendly interface.
* Responses meet the defined response-time target under normal demonstration conditions.
* Answers are grounded in the available official SOP documents.
* If the answer cannot be found in the indexed SOP content, the assistant clearly communicates this.
* Responses use simple and clear operational language.

**US-012**

As a Frontline Picker, I want to know what to do when an item is out of stock or missing from its shelf location so that I can handle the situation correctly without unnecessary delay.

**Acceptance Criteria:**

* The relevant missing-item procedure is indexed in the SOP knowledge base.
* Answer provides step-by-step instructions where the SOP contains them.
* Response includes the appropriate escalation path when the SOP specifies one.

---

## 4. Functional Requirements

Functional requirements define what the system must do. Each requirement should be testable during development and evaluation.

### 4.1 Operations Dashboard

**FR-001:** The system shall display an Operations Overview page showing the following KPIs for the selected store: total orders today, SLA breach rate (%), active orders, active exceptions count, average pick duration, average assignment delay, and inventory accuracy percentage.

**FR-002:** The system shall support automatic refresh of dashboard data at a configurable interval, with 60 seconds as the initial MVP target, without requiring a full page reload.

**FR-003:** The system shall support store filtering, allowing users to view data for individual stores available in the dataset.

**FR-004:** The system shall display KPI values using configurable status indicators to distinguish values within target, approaching threshold, and threshold-exceeded conditions.

**FR-005:** The initial MVP KPI thresholds shall be configurable and use the following proposed operational thresholds:

| KPI                      | Green    | Orange    | Red      |
| ------------------------ | -------- | --------- | -------- |
| SLA Breach Rate          | < 5%     | 5–15%     | > 15%    |
| Average Pick Duration    | < 10 min | 10–20 min | > 20 min |
| Average Assignment Delay | < 5 min  | 5–12 min  | > 12 min |
| Inventory Accuracy       | > 95%    | 85–95%    | < 85%    |

These thresholds are **initial product rules for the MVP** and should be validated or adjusted during testing.

---

### 4.2 SLA Risk Prediction

**FR-006:** The system shall use a trained machine learning model to estimate the probability of SLA breach for supported active orders.

**FR-007:** The system shall classify orders into three risk categories based on the configured breach probability:

* **High Risk:** probability > 0.70
* **Medium Risk:** probability 0.40–0.70
* **Low Risk:** probability < 0.40

These thresholds are initial MVP configuration values and may be adjusted following model evaluation.

**FR-008:** The system shall display the top 3 contributing factors for supported high-risk predictions using model explainability outputs such as SHAP values, translated into plain-language operational explanations.

**FR-009:** The MVP target for the SLA risk prediction model is a minimum ROC-AUC of 0.80 on a held-out test dataset. The achieved metric will be documented after model evaluation.

**FR-010:** The system shall generate SLA risk alerts for orders classified as High Risk and display them in the dashboard's exceptions or risk-monitoring view.

---

### 4.3 Exception Management

**FR-011:** The system shall automatically detect and log exceptions based on configurable operational rules.

Initial rules include:

| Exception Type        | Detection Rule                  | Initial Severity |
| --------------------- | ------------------------------- | ---------------- |
| Slow Pick             | `pick_duration_minutes > 20`    | High             |
| Missing Items         | `items_missing > 0`             | Medium           |
| High Assignment Delay | `assignment_delay_minutes > 15` | High             |
| Inventory Discrepancy | `abs(stock_variance) > 10`      | Medium           |
| Stockout              | `stockout == 'Yes'`             | High             |
| Overloaded Picker     | `tasks_pending > 10`            | Medium           |

These are initial MVP detection rules and may be refined during validation.

**FR-012:** Each exception record shall contain, where applicable: exception ID, exception type, severity, related order/store/employee ID, timestamp detected, current status, and recommended action.

**FR-013:** The system shall allow authorized users to update exception status to: Open, In Progress, Resolved, or Escalated.

**FR-014:** When an exception is marked Resolved, the system shall require the user to enter a resolution note before saving.

---

### 4.4 AI Operations Copilot

**FR-015:** The system shall provide a natural-language interface where users can enter operational questions and receive data-backed answers within the defined response-time target.

**FR-016:** The Copilot shall support questions from at least the following categories:

* Current KPI values — e.g., "What is the SLA breach rate today?"
* Comparative analysis — e.g., "Which store has the highest SLA breach rate?"
* Historical trends — e.g., "How has pick duration changed over the available period?"
* Exception details — e.g., "How many orders are currently at high risk?"
* Resource status — e.g., "How many riders are available at this store?"

**FR-017:** The Copilot shall indicate when a question cannot be answered reliably from the available data rather than generating an unsupported response.

**FR-018:** Where applicable, the Copilot response shall identify the relevant data source, calculation, or dataset used to derive the answer.

---

### 4.5 SOP RAG Assistant

**FR-019:** The system shall maintain a knowledge base of operational Standard Operating Procedures (SOPs) covering, at minimum:

* Inventory discrepancy handling
* Missing item protocol
* SLA breach escalation
* Rider shortage response
* Quality check procedures
* Exception logging

**FR-020:** The RAG system shall retrieve relevant SOP content using semantic search before generating a response, with responses grounded in the indexed documentation.

**FR-021:** The MVP evaluation target is a minimum answer accuracy of 90% on a predefined set of 30 test questions evaluated during user acceptance testing.

**FR-022:** When no relevant SOP content is found for a question, the system shall clearly state that no matching procedure was found rather than generating an unsupported generic answer.

---

## 5. Non-Functional Requirements

Non-functional requirements define how well the system should perform.

**NFR-001 — Performance:**
Dashboard pages shall target a load time of 5 seconds or less under standard demonstration conditions.

**NFR-002 — AI Response Time:**
The AI Copilot shall target a response time of 10 seconds or less for standard operational queries. The SOP RAG Assistant shall target a response time of 5 seconds or less under normal demonstration conditions.

**NFR-003 — Availability:**
The deployed application shall target a minimum of 95% availability during the demonstration and evaluation period, subject to the availability of the selected hosting platform.

**NFR-004 — Accuracy:**
The MVP targets are:

* SLA prediction model: ROC-AUC ≥ 0.80 on the defined held-out test dataset.
* AI Copilot: ≥ 90% correct responses on the predefined evaluation set.
* SOP RAG Assistant: ≥ 90% correct and source-grounded responses on the predefined evaluation set.

Actual achieved metrics shall be documented after evaluation.

**NFR-005 — Usability:**
The dashboard should be usable by users familiar with basic web applications without requiring extensive technical training. Core pages should support responsive layouts for mobile browsers where technically feasible.

**NFR-006 — Reproducibility:**
Code, configuration, documentation, and required synthetic/demo data shall be maintained in the GitHub repository so that another user can reproduce the local setup by following the documented installation instructions.

---

## 6. Requirement Traceability

Each implemented feature should be traceable to one or more user stories and functional requirements. During development, requirement IDs will be used to connect product requirements with implementation tasks, testing activities, and evaluation results.

For example:

| Feature                       | User Story     | Functional Requirement |
| ----------------------------- | -------------- | ---------------------- |
| Operations Overview Dashboard | US-001         | FR-001 to FR-005       |
| SLA Risk Prediction           | US-002         | FR-006 to FR-010       |
| Exception Management          | US-004         | FR-011 to FR-014       |
| AI Operations Copilot         | US-003         | FR-015 to FR-018       |
| SOP RAG Assistant             | US-011, US-012 | FR-019 to FR-022       |

---

---

## 7. MVP Scope Definition

Not everything in this PRD will be built in the first version. The MVP includes only what is necessary to demonstrate the complete value proposition.

### Priority Classification

**P0 — Must Have (MVP Core):**

These features are essential for demonstrating the core MacroOps AI value proposition.

| Feature                            | Justification                                                        |
| ---------------------------------- | -------------------------------------------------------------------- |
| Operations Overview Dashboard      | Core visibility requirement — US-001, FR-001 to FR-005               |
| SLA Risk Prediction with SHAP      | Core prediction requirement — US-002, FR-006 to FR-010               |
| Exception Detection and Management | Core proactive detection — US-004, FR-011 to FR-014                  |
| AI Operations Copilot              | Core natural language access — US-003, FR-015 to FR-018              |
| SOP RAG Assistant                  | Core knowledge access for frontline users — US-011, FR-019 to FR-022 |
| Inventory Status Page              | Core inventory visibility — US-007                                   |
| Business Impact Dashboard          | Required for Phase 03 evaluation                                     |

**P1 — Should Have (Post-MVP):**

These features provide additional value but are not required for the core MVP demonstration.

| Feature                               | Reason Deferred                                              |
| ------------------------------------- | ------------------------------------------------------------ |
| Multi-store comparison view           | Requires more complex data aggregation                       |
| Individual rider performance profiles | Useful extension but not part of the core value proposition  |
| Predictive rider shortage alert       | Builds on the core prediction capability; add if time allows |
| Historical trend analysis             | Requires suitable time-series features in the MVP data       |

**P2 — Nice to Have (Future Roadmap):**

These features are deliberately excluded from the current phase.

| Feature                 | Reason                                               |
| ----------------------- | ---------------------------------------------------- |
| Voice interface         | Out of scope per problem statement                   |
| Multilingual support    | Out of scope per problem statement                   |
| Live system integration | Out of scope — demonstration uses synthetic data     |
| Mobile native app       | Responsive web application is sufficient for the MVP |

---

## 8. Technical Requirements

**TR-001 — Programming Language:**
Python 3.11+.

**TR-002 — Data Storage:**
CSV files will be used for synthetic demonstration data. ChromaDB will be used for vector storage. No production database is required for the MVP.

**TR-003 — ML Framework:**
Scikit-learn and XGBoost will be used for the SLA prediction model, subject to final model evaluation.

**TR-004 — GenAI Stack:**

* **LLM:** Qwen2.5:1.5B via Ollama for local inference
* **Embeddings:** all-MiniLM-L6-v2 via HuggingFace
* **Vector Database:** ChromaDB
* **Framework:** LangChain

**TR-005 — Backend:**
FastAPI will be used to provide REST API endpoints for supported application functionality.

**TR-006 — Frontend:**
Streamlit will be used to build the interactive operations dashboard.

**TR-007 — Deployment:**
Streamlit Community Cloud is the intended deployment target for the demonstration, subject to compatibility, resource limits, and final deployment testing.

**TR-008 — Version Control:**
GitHub will be used to maintain all project code, documentation, configuration, and required synthetic/demo data.

**TR-009 — Research Paper:**
Overleaf (LaTeX) will be used for the research paper and will be updated alongside the technical work.

---

## 9. Data Requirements

**DR-001:**
The system shall use the five synthetic datasets provided for the project:

* `orders.csv` — 100,000 rows
* `picking.csv` — 25,000 rows
* `delivery.csv` — 25,000 rows
* `inventory.csv` — 40,000 rows
* `workforce.csv` — 10,000 rows

**DR-002:**
A master operational dataset shall be created by joining the relevant tables using `order_id` and `store_id` as available keys. Left joins should be used where appropriate to preserve the order-level records required for operational analysis.

**DR-003:**
The SOP knowledge base shall contain a minimum of 8 operational procedure documents covering common exception scenarios and operational workflows.

**DR-004:**
The ML training dataset shall use an 80/20 time-based train/test split where the available data supports a meaningful temporal split, in order to reduce the risk of data leakage.

---

## 10. Assumptions and Constraints

### Assumptions

* The synthetic dataset provides a useful demonstration of representative quick-commerce operational patterns, while not being equivalent to production data.
* Qwen2.5:1.5B is expected to provide sufficient capability for the targeted domain-specific operational queries when supported by relevant RAG context and structured data.
* Streamlit Community Cloud is expected to be suitable for demonstration purposes, subject to final deployment testing and platform resource limitations.

### Constraints

* **Development timeline:** 3 months (September–November 2026)
* **Team:** Single developer (Shivya)
* **Budget:** Zero; the project will prioritize free and open-source tools and services.
* **Hardware:** Personal laptop with CPU-only inference for local GenAI development.

### Risks and Mitigations

* **LLM response quality:** Qwen2.5:1.5B may have limitations due to its model size. This will be mitigated through strong retrieval, constrained prompts, and evaluation.
* **Deployment resource limits:** Streamlit Community Cloud may impose resource limitations. This will be mitigated through efficient data loading, caching, and lightweight application design.
* **Synthetic data limitations:** Synthetic data may not represent all real-world operational edge cases. This limitation will be explicitly acknowledged in the research paper and evaluation.

---

## 11. Out of Scope

The following capabilities are explicitly excluded from MacroOps AI v1.0:

* Real-time integration with live operational systems
* Customer-facing features of any kind
* Payment or financial transaction processing
* Rider navigation and route optimization
* Voice or audio interface
* Non-English language support
* Hardware integrations such as scanners or printers
* Native mobile application

---



