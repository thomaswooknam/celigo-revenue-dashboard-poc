# Executive Revenue & Pipeline Health Dashboard (PoC)
**Live Executive Asset:** `https://public.tableau.com/views/RevenueIntelligenceComplianceDashboard/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link`

---

## 1. Project Purpose & Scope
The objective of this project is to deliver a reliable, self-serve business intelligence dashboard for leadership to track revenue forecasting and pipeline health. 

In fast-growing SaaS environments, executive visibility is frequently compromised by conflicting numbers across departmental reports. This project bridges that gap by establishing strict reporting standards, formalizing metric definitions, and building a trusted data foundation that feeds a production-ready presentation layer.

---

## 2. Executive Problem Statement & Core Hypothesis

### The Ambiguous Business Question:
*"Why do our sales pipeline metrics look completely different depending on which department report we look at, and how much qualified revenue do we actually have pacing for next quarter?"*

### Our Analytical Hypothesis:
We hypothesize that cross-departmental reporting discrepancies are caused by a combination of sales team behavioral shortcuts and legacy CRM system reuse architecture. Specifically, we theorize that:
1. Sales reps bypass historical tracking stages by moving leads from "New" to "Qualified" on the exact day a deal closes, artificially deflating sales cycle duration metrics.
2. The legacy database allows administrators to overwrite dead client records with new company data, which structurally corrupts original system timestamps and skews time-series analytics.

### Confirming the Hypothesis with Data:
To validate this theory, our analytics layer will run programmatic logic checks across the database:
* **To confirm behavioral shortcuts:** We will measure the exact day difference between a lead's creation date and qualification date. If a statistically significant volume of "Qualified" leads show a `0-day` duration, the hypothesis is confirmed.
* **To confirm system reuse corruption:** We will scan for timeline inversions where a record's `created_date` occurs *after* its `qualified_date`. Any positive count confirms historical data overwriting.

---

## 3. Core Functionality & Metric Standards (SOP)
To ensure the dashboard displays a single, audited version of the truth, we implement three core SaaS metrics uniformly calculated within the underlying data mart:

* **Funnel Velocity Index (`days_to_qualify`):** Calculates the precise duration a record takes to advance from ingestion to qualification, explicitly flagging administrative shortcuts to protect true sales cycle averages.
* **Validated Pipeline Revenue:** An audited financial metric that scans the database timeline and automatically zeroes out the estimated deal value of any row exhibiting timestamp corruption, protecting forecasting models from bad data.
* **Pipeline Coverage Ratio:** An operational efficiency metric comparing clean, validated pipeline revenue against the organization's fixed quarterly target ($200,000) to gauge target feasibility.

---

## 4. Technical Execution Steps

### Step A: Mimic the Cloud Warehouse Layer
To simulate a cloud data warehouse (like Snowflake) without infrastructure overhead, we utilize **DuckDB**—a local-first, high-performance analytical database engine. We construct two distinct architectural layers:
1. `raw_crm_leads`: The unstructured landing table containing messy, raw CRM transactional data.
2. `mart_pipeline_analytics`: The production-ready reporting table where data governance rules are applied and business metrics are calculated.

### Step B: Build the Data Mart
We execute a localized SQL script to clean historical records, isolate data integrity anomalies via conditional logic flags, and generate a standardized, flat `.csv` export.

### Step C: Deploy the Self-Serve Dashboard
The audited data asset is plugged directly into **Tableau Public** to build an interactive executive view focusing on revenue pacing, process compliance warnings, and pipeline velocity.

---

## 5. Project Change Log
All adjustments to the business logic, schemas, and metric definitions are logged below to ensure compliance and traceability.

* **2026-05-19:** Project initialized. Defined executive parameters, documented core hypotheses, and mapped out the analytical framework for Celigo's review.
* **2026-05-19:** Developed `warehouse_model.py`. Successfully initialized the local DuckDB mock warehouse layout, executed data integrity validation SQL scripts, and exported verified metrics to `tableau_reporting_data.csv`.
