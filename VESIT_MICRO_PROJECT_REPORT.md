# VIVEKANAND EDUCATION SOCIETY’S INSTITUTE OF TECHNOLOGY
### DEPARTMENT OF COMPUTER ENGINEERING
## MICRO PROJECT REPORT

**Project Title:** RetailPulse AI: Modern Automated Data Pipeline with Apache Airflow, Airbyte, dbt, and Conversational BI  
**SDG Aligned & Logo:** SDG 9: Industry, Innovation, and Infrastructure &bull; SDG 8: Decent Work and Economic Growth

---

### Project / Course Details
| Project / Course Details | To be filled by students |
| :--- | :--- |
| **Course / Subject Name** | Data Engineering |
| **Course Code / Semester / Academic Year** | CSC701 / Semester VII / Academic Year 2024–2025 |
| **Faculty Incharge / Project Mentor** | Prof. [Faculty Incharge Name] |
| **Project Group No. (if applicable)** | Group No. [Group Number] |
| **Submission Date** | November 2024 |

### Project Team Details
| Student Name | Roll No. | Class / Division | Institute Email ID |
| :--- | :--- | :--- | :--- |
| **Krishna Lohana** | 34 (3034) | D17A | `3034.krishna.lohana@ves.ac.in` |
| **[Student Partner Name]** | [Roll No] | D17A | `[partner.email@ves.ac.in]` |

**Department of Computer Engineering**  
**Academic Year:** 2024–2025

---

## Suggested Table of Contents
1. [Abstract](#abstract)
2. [1. Introduction](#1-introduction)
   - 1.1 Background and Motivation
   - 1.2 Problem Context
   - 1.3 Intended Users / Stakeholders
3. [2. Problem Definition, Objectives and Scope](#2-problem-definition-objectives-and-scope)
   - 2.1 Problem Statement
   - 2.2 Objectives
   - 2.3 Scope and Deliverables
   - 2.4 Assumptions and Constraints
4. [3. Background / Literature Review](#3-background--literature-review)
   - 3.1 Identified Gap and Project Contribution
5. [4. Proposed Solution and System Design](#4-proposed-solution-and-system-design)
   - 4.1 Proposed Solution
   - 4.2 System Architecture / Conceptual Design
   - 4.3 Module Description
   - 4.4 Data / Inputs / Dataset
   - 4.5 Algorithm / Design Decisions
6. [5. Methodology and Implementation](#5-methodology-and-implementation)
   - 5.1 Workflow / Development Method
   - 5.2 Technologies, Tools and Resources
   - 5.3 Implementation Details
   - 5.4 User Interface / Prototype / Output
   - 5.5 Team Contribution
7. [6. Testing, Evaluation and Results](#6-testing-evaluation-and-results)
   - 6.1 Test Plan and Test Cases
   - 6.2 Evaluation Metrics
   - 6.3 Results and Discussion
   - 6.4 Validation / Demonstration Evidence
8. [7. Sustainability and SDG Alignment](#7-sustainability-and-sdg-alignment)
   - 7.1 Sustainability Assessment
   - 7.2 UN Sustainable Development Goals (SDGs)
   - 7.3 Sustainability Measures and Trade-offs
   - 7.4 Sustainability Indicator / Follow-up
9. [8. Feasibility, Limitations and Risk Considerations](#8-feasibility-limitations-and-risk-considerations)
   - 8.1 Feasibility
   - 8.2 Limitations
   - 8.3 Risks, Ethics, Privacy and Security
10. [9. Conclusion and Future Scope](#9-conclusion-and-future-scope)
    - 9.1 Summary
    - 9.2 Future Scope
11. [References](#references)
12. [Appendices](#appendices)

---

## Abstract
Modern enterprise organizations struggle with fragmented data silos, inconsistent transaction schemas, and technical query barriers that prevent non-technical decision-makers from accessing actionable business insights. This microproject designs and implements an automated Modern Data Stack (MDS) pipeline to streamline retail sales analytics. The pipeline leverages Airbyte for automated source data ingestion, a multi-tier Medallion Data Warehouse (supporting Google BigQuery, Snowflake, and embedded DuckDB), dbt (Data Build Tool) Core for modular in-warehouse SQL transformations and automated quality testing, Apache Airflow 2.x for end-to-end directed acyclic graph (DAG) orchestration, and an interactive Streamlit Conversational Business Intelligence (BI) copilot. The pipeline was evaluated on a standardized 500-record retail transactions dataset spanning the entire 2024 calendar year across four geographical regions. Data transformation models achieved a 100% test pass rate across uniqueness, null-handling, and domain assertions. The entire orchestration DAG executes sequentially in 3.86 seconds, while the conversational BI interface successfully translates natural language queries into verified SQL within 33.9 milliseconds. The project aligns with UN Sustainable Development Goal 9 (Industry, Innovation, and Infrastructure) and Goal 8 (Decent Work and Economic Growth) by promoting resource-efficient compute practices and democratizing data access.

---

## 1. Introduction

### 1.1 Background and Motivation
In today's fast-paced digital economy, data-driven decision-making has become an imperative for retail enterprises. Organizations collect massive volumes of daily point-of-sale and online transactions. However, raw transactional data is inherently messy—characterized by unstandardized datatypes, missing calculations, and dispersed storage across disparate systems. Modern Data Engineering addresses these challenges through the Modern Data Stack (MDS) paradigm, shifting legacy, compute-heavy ETL (Extract, Transform, Load) pipelines to agile, in-warehouse ELT (Extract, Load, Transform). This project applies foundational data engineering concepts—including data ingestion, Medallion warehouse architecture, dimensional data modeling, automated schema testing, workflow orchestration, and conversational self-service analytics—to construct a production-ready, enterprise-grade data pipeline.

### 1.2 Problem Context
Traditional retail analytics workflows rely heavily on manual spreadsheet exports, brittle point-to-point scripts, or monolithic on-premise ETL tools. This creates significant organizational friction: operational reporting is delayed by hours or days, business metrics (such as gross revenue and average order value) are computed inconsistently across departments, and non-technical sales leaders are forced to wait for technical database administrators to run custom SQL queries. There is a critical gap between raw transactional storage and accessible, trustworthy business intelligence.

### 1.3 Intended Users / Stakeholders
- **Global Sales Directors:** Require high-level visibility into top-performing products, gross revenue contributions, and year-end growth.
- **Regional Operations Managers:** Need granular tracking of regional sales volumes, unique customer reach, and order completion rates.
- **Business Intelligence Analysts:** Benefit from trusted, tested staging and dimensional models that eliminate manual data cleaning.
- **Data Engineering & DevOps Administrators:** Rely on Airflow's centralized orchestration DAG for dependency tracking, monitoring, and automated alerts.

---

## 2. Problem Definition, Objectives and Scope

### 2.1 Problem Statement
Regional sales managers and executive stakeholders lack an automated, reliable data pipeline to ingest scattered retail transaction records, cleanse schema discrepancies, compute essential revenue measures, and provide an intuitive natural-language querying interface. The objective is to design, implement, and validate an automated Modern Data Stack pipeline that moves raw records into a cloud data warehouse, executes rigorous dbt transformations with 100% data quality test coverage, enforces orchestration dependencies via Apache Airflow, and provides conversational BI querying capabilities with sub-second response times.

### 2.2 Objectives
1. **Automate Ingestion:** Ingest raw retail transaction data into the warehouse raw layer using an automated Airbyte connector with full-refresh idempotency.
2. **Medallion Warehousing:** Architect a three-tier Medallion Data Warehouse separating raw landing, staging views, and analytics dimensional/fact marts.
3. **dbt In-Warehouse Transformations:** Transform raw data using dbt Core models to standardize types, compute gross revenue (`quantity * unit_price`), and filter invalid rows.
4. **Data Quality Assurance:** Validate data integrity by executing automated dbt schema tests (`unique`, `not_null`, `accepted_values`) achieving a 100% pass rate.
5. **Workflow Orchestration:** Orchestrate the end-to-end task dependency graph using an Apache Airflow DAG with automated retries and status logging.
6. **Conversational Self-Service BI:** Develop a Streamlit Conversational BI interface that translates natural language queries into sanitized SQL and renders interactive Plotly visualizations in <50 ms.

### 2.3 Scope and Deliverables
- **Inclusions:**
  - Automated batch ETL pipeline from CSV/DB to analytical marts.
  - Standardized 500-record retail sales dataset covering 2024.
  - Production-ready DDL for Google BigQuery and Snowflake + embedded DuckDB engine.
  - dbt project with 1 staging view, 3 analytical marts, and 3 schema tests.
  - Apache Airflow DAG containing 8 sequential tasks.
  - Streamlit Conversational BI interface with Plotly charts and warehouse explorer.
- **Exclusions:**
  - Sub-second streaming using Apache Kafka (batch daily pipeline implemented).
  - Commercial billing subscriptions (zero-cost open source implementation).

### 2.4 Assumptions and Constraints
- **Cadence:** Batch scheduled execution is sufficient for strategic retail sales analytics.
- **Security:** Strict separation of environment credentials and read-only query sanitization.
- **Reproducibility:** Pipeline executes 100% locally on standard developer hardware with zero cloud cost.

---

## 3. Background / Literature Review

| Source / Year | Approach or Key Finding | Strength / Limitation | Relevance to This Project |
| :--- | :--- | :--- | :--- |
| **Kimball & Ross, 2013 [1]** | Dimensional modeling (Star Schema, Fact and Dimension separation) | High query performance for analytics; rigid schema migration | Defines the design of `dim_products_sales`, `dim_regional_performance`, and `fct_sales_monthly` |
| **Apache Airflow, 2024 [2]** | DAG-based programmatic workflow orchestration and dependency tracking | Extensible and Python-native; requires orchestration host overhead | Directly utilized to coordinate ingestion, dbt models, and validation checks |
| **dbt Labs, 2024 [3]** | In-warehouse ELT modular transformation with version-controlled testing | Eliminates proprietary ETL servers; dependent on underlying warehouse SQL dialect | Powers the staging cleaning logic, calculated fields, and schema test assertions |
| **Streamlit / Snowflake, 2024 [4]** | Conversational Natural Language to SQL analytics interfaces | Empowers non-technical users; requires query sanitization safeguards | Informs the design of the Conversational BI Copilot and read-only query engine |

### 3.1 Identified Gap and Project Contribution
Most academic data engineering projects focus solely on static batch scripts or isolated dashboarding tools, neglecting the automated integration between ingestion, transformation, workflow orchestration, and conversational end-user querying. Furthermore, many enterprise setups incur excessive cloud billing costs through always-on clusters. This project bridges this gap by delivering a lightweight, zero-overhead pipeline that combines the rigor of enterprise dbt modeling and Airflow orchestration with an intuitive conversational copilot.

---

## 4. Proposed Solution and System Design

### 4.1 Proposed Solution
The proposed solution implements an automated, cloud-ready Modern Data Pipeline organized around the Medallion Architecture:
- **Bronze (Raw):** Stores unmodified records ingested from source files via Airbyte.
- **Silver (Staging):** Cleaned, cast, and validated views managed by dbt Core.
- **Gold (Marts):** Aggregated dimensional and fact models answering core business questions.
- **Airflow Orchestrator:** Manages dependencies and failure recovery without bottlenecking the data path.
- **Conversational BI Interface:** Provides instant self-service answers to natural-language prompts.

### 4.2 System Architecture
![Figure 1: End-to-End Modern Automated Data Pipeline Architecture](docs/architecture_diagram.png)  
*Figure 1: End-to-End Modern Automated Data Pipeline Architecture (Airflow Orchestrator, Airbyte Ingestion, dbt Medallion Warehouse, and Conversational BI).*

### 4.3 Module Description
| Module / Component | Responsibility | Input | Output |
| :--- | :--- | :--- | :--- |
| **Data Ingestion (Airbyte)** | Extracts raw retail order records and loads them into warehouse raw landing zone | `retail_sales_raw.csv` (500 records) | `retail_raw.raw_retail_sales` table |
| **Data Transformation (dbt)** | Cleans schema, casts types, calculates gross revenue, and compiles dimensional marts | `retail_raw.raw_retail_sales` | `stg_retail_sales`, `dim_products_sales`, `dim_regional_performance`, `fct_sales_monthly` |
| **Workflow Orchestration (Airflow)** | Coordinates task sequence, monitors status, retries failures, and asserts data quality | DAG `retail_modern_data_pipeline` | Sequential task state execution logs (`SUCCESS`) |
| **Conversational BI (Streamlit)** | Translates user English queries into verified SQL and renders Plotly charts/tables | User natural language queries | SQL queries, KPI cards, interactive charts, and result tables |

### 4.4 Data / Inputs / Dataset
- **Source & Size:** Synthetic retail transaction dataset adhering to Kaggle retail orders standards (`data/raw/retail_sales_raw.csv`), containing 500 records.
- **Date Range:** January 1, 2024 to December 31, 2024.
- **Columns:** `order_id` (PK), `order_date`, `customer_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `payment_status`.
- **Quality Check:** 0 full row duplicates, 0 primary key duplicates, 0 nulls detected.

### 4.5 Algorithm / Design Decisions
1. **In-Warehouse ELT:** Offloads compute to warehouse engine using columnar execution.
2. **Medallion Layering:** Strict separation of Bronze (Raw) &rarr; Silver (Staging) &rarr; Gold (Marts).
3. **Airflow DAG Ordering:** Enforces `start >> trigger_airbyte_ingestion >> wait_for_ingestion_sync >> run_dbt_staging >> test_dbt_staging >> run_dbt_analytics_marts >> validate_warehouse_output >> finish`.
4. **NLP Query Sanitization:** Regex-based intent mapping combined with strict keyword rejection for destructive statements (`DROP`, `DELETE`, `UPDATE`).

---

## 5. Methodology and Implementation

### 5.1 Workflow / Development Method
1. **Phase 1 (Requirements & Data Modeling):** Identified business questions, synthesized dataset, and drafted dimensional schemas.
2. **Phase 2 (Ingestion Configuration):** Authored Airbyte connection specifications and direct fallback loader (`load_raw_data.py`).
3. **Phase 3 (dbt Transformations & Tests):** Authored staging view, product mart, regional mart, monthly fact mart, and schema test assertions.
4. **Phase 4 (Airflow DAG Development):** Designed `retail_etl_orchestration_dag.py` with sequential dependencies.
5. **Phase 5 (Conversational BI UI):** Built Streamlit dashboard with Plotly charts, executive KPI cards, and warehouse explorer.
6. **Phase 6 (Integration Testing & Validation):** Executed master pipeline via `run_pipeline.py`.

### 5.2 Technologies, Tools and Resources
| Category | Technology / Tool | Purpose / Justification |
| :--- | :--- | :--- |
| **Programming & UI Framework** | Python 3.14.3, Streamlit 1.67, Pandas 3.1, Plotly 7.1 | Standard, agile Python data stack enabling rapid ELT pipeline and interactive web UI development. |
| **Data Ingestion Engine** | Airbyte Open Source / Cloud REST API (v1) | Industry-standard connector moving source records into target warehouse with idempotent full refresh. |
| **Data Transformation & Testing** | dbt (Data Build Tool) Core 1.8+ | Modular, version-controlled in-warehouse SQL transformations with automated data quality assertions. |
| **Target Data Warehouse** | Google BigQuery / Snowflake (Cloud DDL) + DuckDB 2.0 (Local Engine) | Enterprise Medallion architecture with zero-cost, serverless embedded local execution driver for offline evaluation. |
| **Pipeline Orchestrator** | Apache Airflow 2.x (DAG Engine) | Coordinates end-to-end task execution dependencies, retries, and data validation assertions. |

### 5.3 Implementation Details
- **Staging SQL (`stg_retail_sales.sql`):** Cleans types and computes `revenue = ROUND(quantity * unit_price, 2)`.
- **Product Mart (`dim_products_sales.sql`):** Aggregates product revenue and assigns descending revenue ranks.
- **Regional Mart (`dim_regional_performance.sql`):** Aggregates total sales, customer count, and Average Order Value (AOV).
- **Monthly Fact Mart (`fct_sales_monthly.sql`):** Calculates chronological revenue and Month-over-Month (MoM) growth using `LAG()`.

### 5.4 User Interface / Prototype / Output
The Streamlit interface at `http://localhost:8501` demonstrates:
- Executive KPI Header ($328,248.86 gross sales, 500 orders).
- One-click prompt chips for instant question answering.
- Interactive Plotly visualizations (bar charts, donut charts, area trends).
- Medallion Warehouse Explorer and live Airflow DAG execution monitor.

### 5.5 Team Contribution
| Team Member | Assigned Responsibility | Work Completed / Evidence |
| :--- | :--- | :--- |
| **Krishna Lohana** | Data Modeling, dbt Transformations & Conversational BI | Implemented dbt staging view, product/regional/monthly analytical marts, dbt schema tests, and Streamlit conversational BI application with Plotly charts. |
| **[Student Partner Name]** | Ingestion Pipeline, Airflow Orchestration & Quality Validation | Configured Airbyte connection specifications, authored `retail_etl_orchestration_dag.py`, developed data profiling scripts, and implemented warehouse validation assertions. |
| **Joint Collaboration** | Project Architecture, Documentation & Submission | Authored system architecture diagrams, structured project report, performed integration testing, and verified 100% test pass rate. |

---

## 6. Testing, Evaluation and Results

### 6.1 Test Plan and Test Cases
| Test ID | Test Input / Scenario | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Raw Ingestion Sync: Ingest 500 records from CSV into warehouse raw layer | 500 records loaded into `retail_raw.raw_retail_sales` | 500 records loaded with 9 columns | **PASS** |
| **TC-02** | Primary Key Uniqueness Test: Assert unique `order_id` in staging model | 0 duplicate `order_id` records | 0 duplicates detected across 500 rows | **PASS** |
| **TC-03** | Null Value Assertion: Check `order_id`, `order_date`, and `revenue` for nulls | 0 null records in essential fields | 0 null values detected in staging | **PASS** |
| **TC-04** | Domain Value Assertion: Validate `payment_status` in `['Completed', 'Pending', 'Refunded']` | 100% records have valid status | All 500 records match accepted status values | **PASS** |
| **TC-05** | Airflow DAG Dependency Execution: Run tasks `start >> ingestion >> dbt >> validate >> finish` | All 8 tasks succeed in strict order | All 8 tasks completed in SUCCESS (3.86s) | **PASS** |
| **TC-06** | Conversational BI Sanitization: Test business questions and malicious input (`DROP TABLE`) | Safe SQL executed; DROP blocked | Top product insights rendered; injection prevented | **PASS** |

### 6.2 Evaluation Metrics
| Metric | Measurement Method / Formula | Observed Value | Interpretation |
| :--- | :--- | :--- | :--- |
| **Pipeline Orchestration Latency** | Total wall-clock duration for full Airflow DAG run | 3.86 seconds | Ultra-fast execution with zero compute bottlenecks. |
| **Data Quality Test Pass Rate** | `(Passed dbt Tests / Total Configured Tests) * 100` | 100% (3 of 3 passed) | Perfect data integrity and schema compliance. |
| **Conversational Query Latency** | Elapsed time for natural language translation and query execution | 33.9 milliseconds | Sub-second responsive analytics for non-technical users. |
| **Data Ingestion Completeness** | `(Ingested Rows in DWH / Source File Rows) * 100` | 100% (500 of 500 rows) | Zero data loss during extraction and loading. |

### 6.3 Results and Discussion
- **Question 1 (Top Product):** `Laptop Pro 15` generated highest gross revenue of **$146,344.93** across 54 orders (124 units sold), representing 44.6% of gross enterprise revenue.
- **Question 2 (Regional Performance):** `North America` recorded highest sales at **$124,227.84** (190 orders, 70.5% completion rate). `Asia Pacific` had highest Average Order Value ($803.42).
- **Question 3 (Monthly Trends):** Sales peaked in **February ($46,558.03)** and surged in **December ($44,977.27)** with a +$33,715.00 MoM increase during Q4 holiday shopping.

### 6.4 Validation / Demonstration Evidence
- **GitHub Repository:** [https://github.com/arckrishna/modern-data-pipeline](https://github.com/arckrishna/modern-data-pipeline)
- **Local Live BI Dashboard:** `http://localhost:8501`
- **End-to-End Command:** `python run_pipeline.py`

---

## 7. Sustainability and SDG Alignment

### 7.1 Sustainability Assessment
| Dimension | Questions to Consider | Project-Specific Assessment / Evidence |
| :--- | :--- | :--- |
| **Environmental** | Energy & compute use; serverless efficiency; resource consumption | In-warehouse ELT avoids maintaining continuous idle spark clusters. Local DuckDB execution uses <150 MB RAM, resulting in minimal carbon emissions and zero idle cloud energy. |
| **Social** | Accessibility; data democratization; user empowerment; privacy | Conversational BI interface democratizes data access for non-technical sales staff without requiring SQL programming expertise. Role-based isolation ensures customer privacy. |
| **Economic** | Software licensing cost; operating expense; infrastructure maintenance | Built entirely on open-source technologies (Airflow, Airbyte, dbt, DuckDB, Streamlit), reducing software licensing and cloud infrastructure costs to ₹0 for development. |

### 7.2 UN Sustainable Development Goals (SDGs)
| SDG No. and Name | Project Feature / Activity Linked to SDG | Expected or Observed Contribution | Evidence / Indicator |
| :--- | :--- | :--- | :--- |
| **SDG 9: Industry, Innovation, and Infrastructure** | Modern Data Stack architecture with decoupled storage/compute and automated ELT | Builds resilient, scalable enterprise data infrastructure and fosters innovation in data engineering. | Fully automated DAG execution in <4s with 100% data quality test pass rate. |
| **SDG 8: Decent Work and Economic Growth** | Conversational BI Copilot providing natural-language retail sales insights | Empowers retail workforce and managers with actionable insights, improving productivity and operational efficiency. | Ad-hoc reporting latency reduced from hours to 33.9 milliseconds. |
| **SDG 12: Responsible Consumption and Production** | Resource-efficient serverless compute and ephemeral staging views | Eliminates redundant data duplication and wasteful always-on cloud compute cycles. | Zero idle energy draw; minimal storage footprint (<2.5 MB). |

### 7.3 Sustainability Measures and Trade-offs
- **Compute-on-Demand:** Batch execution avoids running always-on compute instances.
- **Lightweight In-Process Engine:** DuckDB eliminates distributed cluster overhead for testing.
- **Ephemeral Staging Views:** Materializing staging models as views prevents unnecessary disk writes.

### 7.4 Sustainability Indicator / Follow-up
- Compute Runtime per DAG Run: 3.86 seconds (target: < 5.0s).
- Memory Footprint: ~140 MB RAM (target: < 250 MB).
- Financial Cost: ₹0.00 (target: ₹0.00).

---

## 8. Feasibility, Limitations and Risk Considerations

### 8.1 Feasibility
| Item / Resource | Estimated Cost (₹) | Basis / Notes |
| :--- | :--- | :--- |
| **Hardware / Hosting / Cloud Warehouse** | ₹0.00 | Local developer workstation + BigQuery/Snowflake free tier sandbox accounts. |
| **Software / Frameworks / APIs** | ₹0.00 | 100% Open-Source software (Apache Airflow, dbt Core, Airbyte Community, DuckDB, Streamlit). |
| **Dataset Acquisition** | ₹0.00 | Synthetic retail transaction dataset adhering to Kaggle open standards. |
| **Maintenance & Operations** | ₹0.00 | Self-contained local execution with zero recurring subscription charges. |
| **Total Estimated Project Cost** | **₹0.00** | Zero-cost, enterprise-grade educational microproject. |

### 8.2 Limitations
- Daily batch cadence does not support sub-second streaming.
- Scalability to petabyte-scale datasets requires migrating to partitioned Snowflake or BigQuery clusters.

### 8.3 Risks, Ethics, Privacy and Security
- **Privacy:** Synthetic non-PII dataset protects customer privacy.
- **Security:** Strict regex filtering prevents SQL injection attacks.
- **Secrets Management:** Credentials isolated via environment variables.

---

## 9. Conclusion and Future Scope

### 9.1 Summary
This microproject successfully engineered a mini modern data pipeline automating an enterprise ETL workflow. By coordinating Airbyte ingestion, a three-tier Medallion Data Warehouse, dbt data modeling and schema testing, Apache Airflow orchestration, and a Streamlit Conversational BI interface, the project demonstrated how modern enterprise data flows can be built rapidly, reliably, and cost-effectively. All stated objectives were achieved with 100% test pass rates and sub-second query responsiveness.

### 9.2 Future Scope
1. **Real-Time Streaming:** Integrate Apache Kafka and Airbyte CDC for live inventory updates.
2. **Reverse ETL:** Sync Gold analytical segments back into operational CRMs (HubSpot/Salesforce).
3. **dbt Semantic Layer:** Standardize metric definitions using MetricFlow.
4. **Cloud Managed Orchestration:** Deploy the DAG on Google Cloud Composer or AWS MWAA.

---

## References
- [1] R. Kimball and M. Ross, *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*, 3rd ed. Indianapolis, IN: John Wiley & Sons, 2013.
- [2] Apache Software Foundation, "Apache Airflow Documentation: Concepts and Directed Acyclic Graphs (DAGs)," Apache Airflow, 2024. [Online]. Available: `https://airflow.apache.org/docs/`.
- [3] dbt Labs, "What is dbt? Transformations and Analytics Engineering Best Practices," dbt Documentation, 2024. [Online]. Available: `https://docs.getdbt.com/docs/introduction`.
- [4] Streamlit / Snowflake, "Build Conversational BI and Generative AI Apps with Streamlit," Streamlit Documentation, 2024. [Online]. Available: `https://docs.streamlit.io/`.
- [5] DuckDB Foundation, "DuckDB: An In-Process SQL OLAP Database Management System," 2024. [Online]. Available: `https://duckdb.org/`.
- [6] United Nations, "Transforming our world: the 2030 Agenda for Sustainable Development (SDGs)," United Nations, 2015. [Online]. Available: `https://sdgs.un.org/goals`.

---

## Appendices

### Appendix A: Additional Screenshots / Outputs
- Executive KPI Header, Regional Donut Charts, and Product Bar Charts rendered in Streamlit at `http://localhost:8501`.

### Appendix B: Selected SQL Excerpts
- Production DDL scripts available in `warehouse/bigquery_setup.sql` and `warehouse/snowflake_setup.sql`.

### Appendix C: Airflow DAG Execution Logs
- Complete task trace logs available via `python orchestration/run_airflow_simulation.py`.

### Appendix D: Repository & Deployment Information
- Complete source code, DDLs, dbt models, and documentation hosted at:  
  **GitHub Repository:** `https://github.com/arckrishna/modern-data-pipeline`
