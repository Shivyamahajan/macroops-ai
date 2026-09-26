# Product Backlog — MacroOps AI

**Author:** Shivya
**Date:** September 25, 2026
**Last Updated:** September 25, 2026

---

## How to Read This Backlog

* **Priority:** P0 = must have, P1 = should have, P2 = future
* **Size:** S = small (1–2 days), M = medium (3–4 days), L = large (5+ days)
* **Status:** Backlog / In Progress / Done

---

## EPIC 1: Data Foundation

*Everything needed before any model or dashboard can be built*

| ID    | Story                                                | Priority | Size | Status  |
| ----- | ---------------------------------------------------- | -------- | ---- | ------- |
| B-001 | Load and explore all 5 datasets                      | P0       | S    | Backlog |
| B-002 | Write data dictionary for all 5 tables               | P0       | S    | Backlog |
| B-003 | Run data quality checks (missing values, duplicates) | P0       | S    | Backlog |
| B-004 | Create joined master operational dataset             | P0       | S    | Backlog |
| B-005 | Calculate all KPIs from KPI framework                | P0       | M    | Backlog |
| B-006 | Write and run full EDA notebook with visualizations  | P0       | M    | Backlog |

---

## EPIC 2: ML — SLA Risk Prediction

*The core predictive intelligence layer*

| ID    | Story                                                      | Priority | Size | Status  |
| ----- | ---------------------------------------------------------- | -------- | ---- | ------- |
| B-007 | Engineer all features for SLA prediction model             | P0       | M    | Backlog |
| B-008 | Train baseline models (Logistic Regression, RF)            | P0       | S    | Backlog |
| B-009 | Train XGBoost SLA classifier                               | P0       | S    | Backlog |
| B-010 | Evaluate all models with classification report and ROC-AUC | P0       | S    | Backlog |
| B-011 | Run SHAP analysis on best model                            | P0       | S    | Backlog |
| B-012 | Save trained model and scaler as `.pkl` files              | P0       | S    | Backlog |
| B-013 | Write ML model documentation                               | P0       | S    | Backlog |

---

## EPIC 3: Exception Detection Engine

*Automatic detection of operational problems*

| ID    | Story                                                 | Priority | Size | Status  |
| ----- | ----------------------------------------------------- | -------- | ---- | ------- |
| B-014 | Build exception detection rules engine                | P0       | M    | Backlog |
| B-015 | Implement all 6 exception types with severity scoring | P0       | M    | Backlog |
| B-016 | Build exception log data structure                    | P0       | S    | Backlog |
| B-017 | Add recommended action for each exception type        | P0       | S    | Backlog |

---

## EPIC 4: GenAI — SOP Knowledge Base and RAG

*Grounded knowledge retrieval system*

| ID    | Story                                        | Priority | Size | Status  |
| ----- | -------------------------------------------- | -------- | ---- | ------- |
| B-018 | Write all 8 SOP documents for knowledge base | P0       | M    | Backlog |
| B-019 | Build document loading and chunking pipeline | P0       | S    | Backlog |
| B-020 | Create ChromaDB vector store with embeddings | P0       | S    | Backlog |
| B-021 | Build RAG pipeline with MMR retrieval        | P0       | S    | Backlog |
| B-022 | Test RAG with 30 predefined SOP questions    | P0       | S    | Backlog |

---

## EPIC 5: GenAI — AI Operations Copilot

*Natural language interface for operational data*

| ID    | Story                                            | Priority | Size | Status  |
| ----- | ------------------------------------------------ | -------- | ---- | ------- |
| B-023 | Build data query tool functions                  | P0       | M    | Backlog |
| B-024 | Build tool calling framework for Copilot         | P0       | M    | Backlog |
| B-025 | Integrate Qwen2.5 via Ollama                     | P0       | S    | Backlog |
| B-026 | Build conversation memory for multi-turn queries | P0       | S    | Backlog |
| B-027 | Test Copilot with 30 predefined data questions   | P0       | S    | Backlog |

---

## EPIC 6: Streamlit Dashboard

*The user interface for all features*

| ID    | Story                                                  | Priority | Size | Status  |
| ----- | ------------------------------------------------------ | -------- | ---- | ------- |
| B-028 | Build page 1: Operations Overview with KPI cards       | P0       | M    | Backlog |
| B-029 | Build page 2: SLA Risk Monitor with predictions        | P0       | M    | Backlog |
| B-030 | Build page 3: Exception Management with status updates | P0       | M    | Backlog |
| B-031 | Build page 4: Inventory Status                         | P0       | S    | Backlog |
| B-032 | Build page 5: AI Copilot chat interface                | P0       | M    | Backlog |
| B-033 | Build page 6: SOP RAG Assistant                        | P0       | S    | Backlog |
| B-034 | Add sidebar navigation and system status indicators    | P0       | S    | Backlog |
| B-035 | Make all pages responsive for mobile                   | P1       | S    | Backlog |

---

## EPIC 7: FastAPI Backend

*REST API layer for all data and AI functions*

| ID    | Story                                    | Priority | Size | Status  |
| ----- | ---------------------------------------- | -------- | ---- | ------- |
| B-036 | Build `/api/operations/summary` endpoint | P0       | S    | Backlog |
| B-037 | Build `/api/orders/at-risk` endpoint     | P0       | S    | Backlog |
| B-038 | Build `/api/exceptions/active` endpoint  | P0       | S    | Backlog |
| B-039 | Build `/api/copilot/query` endpoint      | P0       | S    | Backlog |
| B-040 | Build `/api/rag/query` endpoint          | P0       | S    | Backlog |
| B-041 | Write API documentation                  | P0       | S    | Backlog |

---

## EPIC 8: Testing and Evaluation

*Formal quality assurance*

| ID    | Story                                                     | Priority | Size | Status  |
| ----- | --------------------------------------------------------- | -------- | ---- | ------- |
| B-042 | Write functional test plan with test cases                | P0       | M    | Backlog |
| B-043 | Execute GenAI evaluation (accuracy, hallucination, speed) | P0       | M    | Backlog |
| B-044 | Execute UAT with 4 predefined scenarios                   | P0       | S    | Backlog |
| B-045 | Document test results and defects found                   | P0       | S    | Backlog |

---

## EPIC 9: Deployment and Documentation

*Making it deployable and documented*

| ID    | Story                                                            | Priority | Size | Status  |
| ----- | ---------------------------------------------------------------- | -------- | ---- | ------- |
| B-046 | Prepare `requirements.txt` and installation guide                | P0       | S    | Backlog |
| B-047 | Evaluate and, if compatible, deploy to Streamlit Community Cloud | P0       | S    | Backlog |
| B-048 | Complete README with badges and screenshots                      | P0       | S    | Backlog |
| B-049 | Write business impact analysis                                   | P0       | M    | Backlog |
| B-050 | Complete research paper on Overleaf                              | P0       | L    | Backlog |
| B-051 | Prepare final presentation deck                                  | P0       | M    | Backlog |
| B-052 | Final GitHub cleanup and documentation                           | P0       | S    | Backlog |

---

## Backlog Summary

| Epic                  | Total Items |     P0 |    P1 |    P2 |
| --------------------- | ----------: | -----: | ----: | ----: |
| 1. Data Foundation    |           6 |      6 |     0 |     0 |
| 2. ML Prediction      |           7 |      7 |     0 |     0 |
| 3. Exception Engine   |           4 |      4 |     0 |     0 |
| 4. RAG Knowledge Base |           5 |      5 |     0 |     0 |
| 5. AI Copilot         |           5 |      5 |     0 |     0 |
| 6. Dashboard          |           8 |      7 |     1 |     0 |
| 7. FastAPI            |           6 |      6 |     0 |     0 |
| 8. Testing            |           4 |      4 |     0 |     0 |
| 9. Deployment         |           7 |      7 |     0 |     0 |
| **TOTAL**             |      **52** | **51** | **1** | **0** |

---


