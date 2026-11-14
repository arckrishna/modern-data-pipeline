# Airbyte / Fivetran Ingestion Configuration Guide

This guide documents the enterprise ingestion setup for the **Retail Sales Analytics Modern Data Pipeline** using **Airbyte** (Open Source / Cloud) or **Fivetran**.

---

## 1. Architectural Role in the Pipeline
- **Source**: File / CSV Source (or PostgreSQL relational database populated with `retail_sales_raw.csv`).
- **Destination**: Cloud Data Warehouse (Snowflake / Google BigQuery) or Local DuckDB analytical store.
- **Sync Mode**: `Full Refresh | Overwrite` (or `Incremental | Append` for production streaming).
- **Trigger**: Orchestrated via Apache Airflow's `AirbyteTriggerSyncOperator` calling Airbyte REST API v1.

---

## 2. Airbyte Step-by-Step Setup

### Step A: Source Configuration
1. Open the Airbyte UI (e.g., `http://localhost:8000` or `cloud.airbyte.com`).
2. Navigate to **Sources** &rarr; **New Source**.
3. Select **File (CSV)** or **Local CSV / S3 / Google Sheets**:
   - **Source Name**: `retail_csv_source`
   - **URL / Storage Provider**: Local Mount or S3 Bucket / HTTPS link to `data/raw/retail_sales_raw.csv`
   - **Format**: `CSV`
   - **Delimiter**: `,`
   - **Header**: `true`
4. Click **Set up source** and wait for connection testing to pass.

### Step B: Destination Configuration
#### Option 1: Snowflake Destination
- **Destination Type**: `Snowflake`
- **Host**: `<account_identifier>.snowflakecomputing.com`
- **Role**: `RETAIL_TRANSFORMER_ROLE`
- **Warehouse**: `RETAIL_WH`
- **Database**: `RETAIL_DWH`
- **Default Schema**: `RAW_LAYER`
- **Username / Password / Private Key**: Configured in `.env` (kept out of repository).

#### Option 2: Google BigQuery Destination
- **Destination Type**: `BigQuery`
- **Project ID**: `<gcp-project-id>`
- **Default Dataset ID**: `retail_raw`
- **Authentication**: Service Account JSON Key (GCP IAM with BigQuery Admin/Editor permissions).

### Step C: Connection & Sync Settings
1. Go to **Connections** &rarr; **New Connection**.
2. Select Source `retail_csv_source` and Destination `Snowflake_Destination` / `BigQuery_Destination`.
3. Configure Stream:
   - Stream Name: `raw_retail_sales`
   - Sync Frequency: **Manual** (Orchestration is delegated entirely to Apache Airflow).
   - Sync Mode: `Full Refresh | Overwrite` (ensures idempotency on each DAG run).
4. Save the Connection and note down the **Connection ID** (UUID) for Airflow DAG configuration.

---

## 3. Airbyte REST API Triggering (Airflow Integration)
Airflow triggers the synchronization programmatically using:
- **Endpoint**: `POST /api/v1/connections/sync`
- **Payload**: `{"connectionId": "<YOUR_AIRBYTE_CONNECTION_ID>"}`
- **Operator**: `airflow.providers.airbyte.operators.airbyte.AirbyteTriggerSyncOperator`

When Airbyte server is offline or when running in localized environments, the pipeline seamlessly falls back to `ingestion/load_raw_data.py`, ensuring 100% reproducible execution.
