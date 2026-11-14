-- =============================================================================
-- DATA ENGINEERING MICROPROJECT - TARGET DATA WAREHOUSE SETUP (SNOWFLAKE)
-- =============================================================================
-- Scenario: Retail Sales Analytics Modern Data Pipeline
-- Authors: Microproject Group
-- Target: Snowflake Data Cloud (Standard / Free-Trial / Student Edition)
-- =============================================================================

-- Step 3.1: Create Compute Warehouse
CREATE OR REPLACE WAREHOUSE RETAIL_WH
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Virtual warehouse for retail ETL ingestion, dbt models, and BI queries';

-- Step 3.2: Create Dedicated Database
CREATE OR REPLACE DATABASE RETAIL_DWH
    COMMENT = 'Central repository for retail modern data pipeline';

USE DATABASE RETAIL_DWH;

-- Step 3.3: Create Layer Schemas (Medallion Architecture)
-- 1. RAW_LAYER: Destination for Airbyte / Fivetran raw ingestion
CREATE OR REPLACE SCHEMA RAW_LAYER
    COMMENT = 'Landing zone for raw ingested tables from source connectors';

-- 2. STAGING_LAYER: Cleaned, type-cast, filtered data managed by dbt
CREATE OR REPLACE SCHEMA STAGING_LAYER
    COMMENT = 'Staging zone with standardized schema, clean types, and valid records';

-- 3. ANALYTICS_LAYER: Dimensional, fact, and aggregated marts for BI consumption
CREATE OR REPLACE SCHEMA ANALYTICS_LAYER
    COMMENT = 'Consumption marts for BI dashboarding, executive metrics, and conversational query interface';

-- Step 3.4: Create Raw Ingestion Destination Table in RAW_LAYER
USE SCHEMA RAW_LAYER;

CREATE OR REPLACE TABLE RAW_RETAIL_SALES (
    order_id VARCHAR(50),
    order_date VARCHAR(50),
    customer_id VARCHAR(50),
    product VARCHAR(150),
    category VARCHAR(100),
    region VARCHAR(100),
    quantity VARCHAR(50),
    unit_price VARCHAR(50),
    payment_status VARCHAR(50),
    _ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Step 3.5: Configure Role & Access Control for Airbyte & dbt
USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE ROLE RETAIL_TRANSFORMER_ROLE;
GRANT USAGE ON WAREHOUSE RETAIL_WH TO ROLE RETAIL_TRANSFORMER_ROLE;
GRANT ALL PRIVILEGES ON DATABASE RETAIL_DWH TO ROLE RETAIL_TRANSFORMER_ROLE;
GRANT ALL PRIVILEGES ON ALL SCHEMAS IN DATABASE RETAIL_DWH TO ROLE RETAIL_TRANSFORMER_ROLE;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN DATABASE RETAIL_DWH TO ROLE RETAIL_TRANSFORMER_ROLE;
