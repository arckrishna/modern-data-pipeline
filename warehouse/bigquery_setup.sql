-- =============================================================================
-- DATA ENGINEERING MICROPROJECT - TARGET DATA WAREHOUSE SETUP (GOOGLE BIGQUERY)
-- =============================================================================
-- Scenario: Retail Sales Analytics Modern Data Pipeline
-- Authors: Microproject Group
-- Target: Google Cloud BigQuery (Free Tier / Sandbox / Student Account)
-- =============================================================================

-- Step 3.1: Create Datasets representing Pipeline Layers (Medallion Architecture)
-- Run in Google Cloud Console or via bq CLI

-- 1. Raw ingestion dataset (Airbyte / Fivetran destination)
CREATE SCHEMA IF NOT EXISTS `retail_raw`
OPTIONS (
    location = "US",
    description = "Raw ingested retail sales data from source files/connectors"
);

-- 2. Staging dataset for dbt cleaned models
CREATE SCHEMA IF NOT EXISTS `retail_staging`
OPTIONS (
    location = "US",
    description = "Cleaned, standardized, and validated staging models built by dbt"
);

-- 3. Analytics dataset for consumption marts and Conversational BI
CREATE SCHEMA IF NOT EXISTS `retail_analytics`
OPTIONS (
    location = "US",
    description = "Aggregated business marts for Streamlit conversational BI and queries"
);

-- Step 3.2: Create Raw Landing Table in retail_raw
CREATE OR REPLACE TABLE `retail_raw.raw_retail_sales` (
    order_id STRING,
    order_date STRING,
    customer_id STRING,
    product STRING,
    category STRING,
    region STRING,
    quantity STRING,
    unit_price STRING,
    payment_status STRING,
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
OPTIONS (
    description = "Raw ingested sales transactions from Airbyte"
);
