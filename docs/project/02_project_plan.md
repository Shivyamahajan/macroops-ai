# Project Plan — MacroOps AI
**Author:** Shivya
**Date:** September 28, 2026
**Version:** 1.0

---

## Project Overview

| Item | Detail |
|------|--------|
| Project Name | MacroOps AI — Intelligent Operations Management Platform |
| Author | Shivya |
| Mentor | Sagar Sakalley, MacroEdtech |
| Start Date | September 14, 2026 |
| End Date | November 30, 2026 |
| Total Duration | 11 weeks |
| Progress Reviews | Every 15 days (6 reviews total) |

---

## Phase Overview

| Phase | Weeks | Dates | Focus |
|-------|-------|-------|-------|
| Month 1: Discovery | Weeks 1-3 | Sep 14 – Oct 1 | Business, Product, Planning |
| Month 2: Development | Weeks 4-7 | Oct 5 – Nov 1 | Data, ML, GenAI, Dashboard |
| Month 3: Delivery | Weeks 8-11 | Nov 2 – Nov 30 | Testing, Deployment, Impact |

---

## Detailed Week-by-Week Plan

### MONTH 1 — Business Discovery and Product Strategy

---

#### Week 1 (Sep 14–19) — Business Foundation ✅ COMPLETE
| Task | Deliverable | Status |
|------|-------------|--------|
| Industry research | docs/business/01_industry_research.md | ✅ Done |
| AS-IS process map | docs/business/02_as_is_process_map.md | ✅ Done |
| Pain point analysis | docs/business/03_pain_point_analysis.md | ✅ Done |
| Business problem statement | docs/business/04_business_problem_statement.md | ✅ Done |
| Stakeholder map and personas | docs/product/01_stakeholder_map_and_personas.md | ✅ Done |

---

#### Week 2 (Sep 21–26) — Product Strategy ✅ COMPLETE
| Task | Deliverable | Status |
|------|-------------|--------|
| User journey maps | docs/product/02_user_journey_maps.md | ✅ Done |
| Product vision | docs/product/03_product_vision.md | ✅ Done |
| Product Requirements Document | docs/product/04_PRD.md | ✅ Done |
| Product backlog | docs/project/01_product_backlog.md | ✅ Done |

---

#### Week 3 (Sep 28–Oct 1) — Project Planning ← CURRENT
| Task | Deliverable | Status |
|------|-------------|--------|
| Project plan | docs/project/02_project_plan.md | 🔄 In Progress |
| GitHub Projects setup | Kanban board with all 52 items | 🔄 In Progress |
| Progress deck for Sagar | 10-slide presentation | 🔄 In Progress |
| Month 1 retrospective | docs/project/03_month1_retrospective.md | Pending |

---

### MONTH 2 — Data Engineering, ML, GenAI, Dashboard

---

#### Week 4 (Oct 5–11) — Data Foundation and EDA
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Load and explore all 5 datasets | B-001 | Python script output |
| Write complete data dictionary | B-002 | docs/technical/data_dictionary.md |
| Run data quality checks | B-003 | docs/technical/data_quality_report.md |
| Create master joined dataset | B-004 | data/processed/master_operational.csv |
| Calculate all KPIs | B-005 | src/analytics/kpi_calculator.py |
| Write full EDA notebook | B-006 | notebooks/01_EDA.ipynb |

---

#### Week 5 (Oct 12–18) — Streamlit Analytics Dashboard
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Build Operations Overview page | B-028 | src/app/pages/01_overview.py |
| Build Inventory Status page | B-031 | src/app/pages/04_inventory.py |
| Add sidebar and navigation | B-034 | src/app/main.py |
| Build Exception Detection engine | B-014 to B-017 | src/analytics/exception_engine.py |
| Build Exception Management page | B-030 | src/app/pages/03_exceptions.py |

---

#### Week 6 (Oct 19–25) — ML Model for SLA Prediction
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Feature engineering for SLA model | B-007 | src/ai/feature_engineering.py |
| Train baseline models | B-008 | notebooks/02_ML_Baseline.ipynb |
| Train XGBoost classifier | B-009 | models/xgboost_sla.pkl |
| Evaluate and compare all models | B-010 | reports/ml_evaluation.csv |
| SHAP analysis on best model | B-011 | reports/figures/shap_plots |
| Save model and scaler | B-012 | models/ folder |
| Build SLA Risk Monitor page | B-029 | src/app/pages/02_sla_risk.py |

---

#### Week 7 (Oct 26–Nov 1) — GenAI Components
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Write all 8 SOP documents | B-018 | data/knowledge_base/ (8 files) |
| Build document chunking pipeline | B-019 | src/ai/build_knowledge_base.py |
| Create ChromaDB vector store | B-020 | data/vector_db/ |
| Build RAG pipeline | B-021 | src/ai/rag_pipeline.py |
| Test RAG with 30 questions | B-022 | reports/rag_evaluation.csv |
| Build Copilot data tools | B-023 to B-024 | src/ai/copilot_tools.py |
| Integrate Qwen2.5 via Ollama | B-025 | src/ai/llm_setup.py |
| Build conversation memory | B-026 | src/ai/conversational_copilot.py |
| Test Copilot with 30 questions | B-027 | reports/copilot_evaluation.csv |
| Build AI Copilot dashboard page | B-032 | src/app/pages/05_copilot.py |
| Build SOP RAG Assistant page | B-033 | src/app/pages/06_sop_assistant.py |

---

### MONTH 3 — Testing, Deployment, Business Impact

---

#### Week 8 (Nov 2–8) — FastAPI Backend and Integration
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Build all FastAPI endpoints | B-036 to B-040 | src/app/api.py |
| Write API documentation | B-041 | docs/technical/api_documentation.md |
| End-to-end integration testing | B-042 | All pages connected and working |
| Fix any integration bugs | - | Clean working application |

---

#### Week 9 (Nov 9–15) — Formal Testing and GenAI Evaluation
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Write complete test plan | B-042 | docs/testing/test_plan.md |
| Execute GenAI evaluation | B-043 | reports/genai_evaluation_report.md |
| Execute UAT scenarios | B-044 | reports/uat_results.md |
| Document all defects and fixes | B-045 | docs/testing/defect_log.md |

---

#### Week 10 (Nov 16–22) — Deployment and Business Impact
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Prepare for deployment | B-046 | requirements.txt, install guide |
| Evaluate and, if compatible, deploy to Streamlit Community Cloud | B-047 | Live URL if deployment is compatible |
| Write business impact analysis | B-049 | reports/business_impact.md |
| Complete research paper | B-050 | Overleaf PDF final draft |
| Clean up GitHub repository | B-052 | Professional README with screenshots |

---

#### Week 11 (Nov 23–30) — Final Presentation and Submission
| Task | Backlog ID | Deliverable |
|------|-----------|-------------|
| Build final presentation deck | B-051 | 15-slide PPT or PDF |
| Final GitHub polish | B-048, B-052 | Complete professional repository |
| Prepare live demo script | - | Demo walkthrough document |
| Final submission to Sagar | - | All deliverables packaged |

---

## Progress Review Schedule

| Review | Date | Format | What to Present |
|--------|------|--------|-----------------|
| Review 1 | ~Sep 28 | Google Meet / Video | Month 1 Week 1-2 complete |
| Review 2 | ~Oct 12 | Google Meet / Video | Data foundation, EDA, dashboard start |
| Review 3 | ~Oct 26 | Google Meet / Video | ML model, SHAP, first dashboard pages live |
| Review 4 | ~Nov 9 | Google Meet / Video | GenAI components, full dashboard, testing started |
| Review 5 | ~Nov 23 | Google Meet / Video | Deployment live, business impact complete |
| Review 6 | ~Nov 30 | Google Meet / Video | Final submission and demonstration |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Qwen2.5:1.5B insufficient quality | Medium | High | Use RAG to compensate for model size |
| Streamlit Cloud resource limits | Low | Medium | Optimize with st.cache_data throughout |
| ML model accuracy below target | Low | High | Tune hyperparameters, try multiple models |
| Time pressure in Month 3 | Medium | Medium | Keep Month 2 on schedule, no scope creep |
| Overleaf paper falling behind | Medium | Medium | Write 30 minutes every week without exception |

---

## Key Milestones

| Milestone | Target Date | Description |
|-----------|------------|-------------|
| M1 — Product Design Complete | Oct 1 | All PRD and backlog documents done |
| M2 — Data Foundation Ready | Oct 11 | All 5 datasets explored, joined, KPIs calculated |
| M3 — Dashboard v1 Live | Oct 18 | Operations overview and exceptions pages working |
| M4 — ML Model Complete | Oct 25 | SLA prediction trained, evaluated, SHAP done |
| M5 — GenAI Layer Complete | Nov 1 | RAG and Copilot both working |
| M6 — Full MVP Working | Nov 8 | All pages integrated, FastAPI working |
| M7 — Testing Complete | Nov 15 | All evaluation done, defects fixed |
| M8 — Deployment Evaluated | Nov 22 | Streamlit Community Cloud deployment evaluated; live deployment if compatible |
| M9 — Final Submission | Nov 30 | Paper, repo, presentation all submitted |