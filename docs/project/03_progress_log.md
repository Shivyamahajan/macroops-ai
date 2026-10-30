# Progress Log — MacroOps AI

**Author:** Shivya

This log records daily progress throughout the project.
Updated every working day.

---

## Month 1 — September 2026

### Week 1 (Sep 14–19) — Business Foundation

**Sep 14:**

* Created GitHub repository `macroops-ai`
* Set up the complete project folder structure
* Copied dummy operational datasets to `data/dummy/`
* Wrote the initial `README.md`
* Started industry research on quick-commerce operations

**Sep 15:**

* Completed industry research document
* Created AS-IS process map using an 8-lane swimlane structure
* Exported the process diagram to `reports/figures/`

**Sep 16:**

* Ran the pain point analysis Python script
* Identified key operational metrics including 89.7% SLA breach rate, 13.03-minute average picking duration, and 8.17-minute average rider assignment delay
* Wrote the complete pain point analysis document using verified dataset results

**Sep 17:**

* Wrote the business problem statement
* Defined the business problem, scope boundaries, and success metrics

**Sep 18:**

* Wrote the stakeholder map
* Created four representative user personas: Rahul, Priya, Arjun, and Amit

**Sep 19:**

* Reviewed all Week 1 documents for completeness
* Pushed Week 1 work to GitHub
* Updated Overleaf with the Business Context and Problem Analysis section

---

### Week 2 (Sep 21–26) — Product Strategy

**Sep 21:**

* Created four representative future-state user journey maps
* Identified expected user needs, workflow improvements, and product opportunities for each persona

**Sep 22:**

* Wrote the Product Vision document
* Defined five core product principles
* Defined target success outcomes for the three-month project

**Sep 23:**

* Wrote PRD Part 1
* Defined 12 user stories with acceptance criteria
* Defined functional requirements FR-001 to FR-022 and non-functional requirements

**Sep 24:**

* Wrote PRD Part 2
* Defined MVP scope, technical requirements, data requirements, assumptions, constraints, and out-of-scope items

**Sep 25:**

* Created the complete product backlog
* Defined 52 backlog items across 9 epics
* Classified backlog items by priority

**Sep 26:**

* Completed the Week 2 documentation review
* Verified user stories, functional requirements, MVP scope, and backlog
* Pushed Week 2 documentation to GitHub
* Updated README with Week 2 completion status
* Updated Overleaf with the Product Design and Requirements section

---

### Week 3 (Sep 28–Oct 1) — Project Planning

**Sep 28:**

* Created the three-month project plan and timeline
* Documented task dependencies, weekly development activities, progress reviews, risks, and key milestones
* Reviewed and aligned the project schedule with the product backlog

**Sep 29:**

* Created the running project progress log
* Began setting up the Agile project management structure using GitHub Projects

**Sep 30:**

- Completed the Agile project management board setup in GitHub Projects.
- Configured the five-column workflow: Backlog, This Week, In Progress, In Review, and Done.
- Created and configured project-specific Epic and Priority labels.
- Added all 52 product backlog items (B-001 to B-052) to the GitHub Project board.
- Verified that all 52 backlog items were visible and organized in the Backlog column.

**Oct 1:**

- Reviewed the project backlog and prepared for the upcoming data foundation and exploratory data analysis work.

---

## Month 2 — October 2026

### Week 4 (Oct 5–9) — Data Foundation and Exploratory Analysis

**Oct 5:**

* Loaded and inspected the five synthetic operational datasets: orders, picking, delivery, inventory, and workforce
* Confirmed 200,000 source records across the five datasets
* Ran the data quality report; all five source tables reported zero missing values and zero duplicate rows under the implemented checks

**Oct 6:**

* Created the integrated master operational dataset at `data/processed/master_operational_all_tables.csv`
* Preserved 100,000 unique orders in the master dataset, with 49 columns
* Documented unmatched picking and delivery records resulting in missing joined features
* Implemented and ran the operational KPI calculator

**Oct 7:**

* Completed EDA Notebook Part 1 (Cells 1–6)
* Generated visualizations for order status, hourly SLA performance, store performance, picking, and delivery

**Oct 8:**

* Completed EDA Notebook Part 2 (Cells 7–12)
* Analyzed inventory accuracy, store-level inventory performance, and workforce workload
* Generated a feature correlation matrix and operational exception summary
* Completed the EDA summary and verified that all 10 EDA figure files exist

**Oct 9:**

* Verified the data loading, data quality, master dataset, and KPI calculator scripts
* Completed and saved all 10 EDA visualizations
* Committed the EDA notebook, progress log, and analysis figures to   GitHub (commit 4546d25)
* Pushed the changes successfully to the main branch
* Updated the GitHub Projects board: moved B-001 to B-006 to Done and B-028, B-030, B-031, and B-034 to This Week

### Week 5 (Oct 12–16) — Operations Dashboard Development

**Oct 12:**

* Reviewed the integrated operational datasets and existing KPI calculations.
* Reviewed the Operations Overview dashboard requirements and layout.
* Planned the presentation of key operational metrics and performance visualizations.

**Oct 13:**

* Developed and refined the Exception Management dashboard.
* Integrated exception detection results into the dashboard.
* Added exception severity summaries, filtering options, and exception details.
* Implemented CSV export functionality for exception records.

**Oct 14:**

* Developed the Inventory Status dashboard.
* Added inventory accuracy, stockout, negative variance, and high variance KPIs.
* Added inventory analysis visualizations and store-level health information.
* Implemented an adjustable inventory accuracy threshold.

**Oct 15:**

* Integrated the Operations Overview, Exception Management, and Inventory Status pages into the Streamlit application.
* Configured sidebar navigation between the three dashboard pages.
* Tested dashboard functionality and reviewed KPI displays, charts, filters, and tables.
* Fixed navigation and application issues identified during testing.

**Oct 16:**

* Reviewed all three dashboard pages: Operations Overview, Exception Management, and Inventory Status.
* Reviewed the Week 5 implementation and prepared documentation updates.
* Prepared the completed dashboard work for GitHub synchronization and project board updates.

### **Oct 19 — Day 1: Feature Engineering**

* Inspected the master operational dataset containing 100,000 records and 22 columns.
* Identified and reviewed relevant features for SLA breach prediction.
* Implemented the feature engineering pipeline in `src/ai/feature_engineering.py`.
* Created 11 model-ready features, including order details, SLA window, picking metrics, and delivery metrics.
* Excluded outcome-related columns to reduce target leakage.
* Prepared a time-based training, validation, and test split.
* Generated an ML dataset containing 25,000 eligible orders.

### **Oct 20 — Day 2: SLA Prediction Model Training**

* Implemented the model training pipeline in `src/ai/train_sla_model.py`.
* Trained and compared four models: Majority Baseline, Logistic Regression, Random Forest, and XGBoost.
* Evaluated model performance using Accuracy, ROC-AUC, PR-AUC, Precision, Recall, and F1-score.
* Selected Logistic Regression based on validation ROC-AUC.
* Achieved a test ROC-AUC of 0.6197 against the PRD target of 0.80.
* Identified class imbalance and model generalization challenges during evaluation.
* Saved the trained model and validation-based risk cutoffs in `models/sla_model.pkl`.
* Generated the model evaluation report and visualization.

### **Oct 21 — Day 3: SHAP Explainability**

* Implemented global SHAP explainability in `src/ai/shap_analysis.py`.
* Generated SHAP feature importance bar and summary dot plots.
* Exported mean absolute SHAP feature importance to CSV.
* Developed `src/ai/sla_predictor.py` for individual order risk scoring and explanations.
* Implemented Low, Medium, and High SLA risk classification using saved risk cutoffs.
* Added individual order explanations identifying the top contributing features and suggested operational actions.
* Successfully tested the predictor on sample test orders and verified all generated files.

### **Oct 22 — Day 4: SLA Risk Monitor**

* Created and integrated the SLA Risk Monitor Streamlit page.
* Scored 5,000 historical test orders using Logistic Regression.
* Added risk summaries, interactive charts, and high-risk order filtering.
* Integrated SHAP-based explanations and suggested operational actions.
* Displayed historical SLA outcomes and clarified that predictions are not live.
* Successfully tested all four dashboard pages and captured screenshots.