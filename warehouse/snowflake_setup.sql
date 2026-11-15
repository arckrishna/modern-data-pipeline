-- =============================================================================
-- RETAILPULSE AI: TARGET DATA WAREHOUSE DDL (SNOWFLAKE DATA CLOUD)
-- =============================================================================
-- Subject: Data Engineering Microproject
-- Target: Snowflake Data Cloud (Standard / Free-Trial / Student Edition)
-- Architecture: Medallion Architecture (Bronze -> Silver -> Gold)
-- =============================================================================

-- Step 1: Provision Virtual Compute Warehouse
CREATE OR REPLACE WAREHOUSE RETAIL_WH
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Dedicated compute warehouse for RetailPulse AI ingestion, dbt models, and BI queries';

-- Step 2: Provision Dedicated Database
CREATE OR REPLACE DATABASE RETAIL_DWH
    COMMENT = 'Central repository for retail modern data pipeline';

USE DATABASE RETAIL_DWH;

-- Step 3: Provision Layer Schemas (Medallion Architecture)
-- 3.1 RAW_LAYER (Bronze): Destination for Airbyte raw ingestion
CREATE OR REPLACE SCHEMA RAW_LAYER
    COMMENT = 'Bronze landing zone for raw ingested tables from source connectors';

-- 3.2 STAGING_LAYER (Silver): Cleaned, type-cast, filtered views managed by dbt
CREATE OR REPLACE SCHEMA STAGING_LAYER
    COMMENT = 'Silver staging zone with standardized schema, clean types, and valid records';

-- 3.3 ANALYTICS_LAYER (Gold): Dimensional, fact, and aggregated marts for BI consumption
CREATE OR REPLACE SCHEMA ANALYTICS_LAYER
    COMMENT = 'Gold consumption marts for RetailPulse AI conversational BI dashboard';

-- =============================================================================
-- STEP 4: BRONZE TIER (RAW LANDING TABLE)
-- =============================================================================
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

-- =============================================================================
-- STEP 5: SILVER TIER (STAGING CLEANED VIEW)
-- =============================================================================
USE SCHEMA STAGING_LAYER;

CREATE OR REPLACE VIEW STG_RETAIL_SALES AS
SELECT
    TRIM(order_id) AS order_id,
    TO_DATE(order_date, 'YYYY-MM-DD') AS order_date,
    TRIM(customer_id) AS customer_id,
    TRIM(product) AS product_name,
    TRIM(category) AS category,
    TRIM(region) AS region,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(unit_price AS DECIMAL(10, 2)) AS unit_price,
    ROUND(CAST(quantity AS INTEGER) * CAST(unit_price AS DECIMAL(10, 2)), 2) AS revenue,
    TRIM(payment_status) AS payment_status,
    _ingested_at
FROM RETAIL_DWH.RAW_LAYER.RAW_RETAIL_SALES
WHERE order_id IS NOT NULL
  AND CAST(quantity AS INTEGER) > 0
  AND CAST(unit_price AS DECIMAL(10, 2)) > 0;

-- =============================================================================
-- STEP 6: GOLD TIER (ANALYTICS MARTS)
-- =============================================================================
USE SCHEMA ANALYTICS_LAYER;

-- Mart 1: Product Revenue & Ranking (Answers Business Question 1)
CREATE OR REPLACE TABLE DIM_PRODUCTS_SALES AS
SELECT
    product_name,
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN payment_status = 'Completed' THEN revenue ELSE 0 END), 2) AS completed_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM RETAIL_DWH.STAGING_LAYER.STG_RETAIL_SALES
GROUP BY product_name, category
ORDER BY total_revenue DESC;

-- Mart 2: Regional Performance & AOV (Answers Business Question 2)
CREATE OR REPLACE TABLE DIM_REGIONAL_PERFORMANCE AS
SELECT
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value,
    ROUND(SUM(CASE WHEN payment_status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS completion_rate_pct,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS regional_rank
FROM RETAIL_DWH.STAGING_LAYER.STG_RETAIL_SALES
GROUP BY region
ORDER BY total_revenue DESC;

-- Mart 3: Monthly Fact Trends & MoM Growth (Answers Business Question 3)
CREATE OR REPLACE TABLE FCT_SALES_MONTHLY AS
WITH monthly AS (
    SELECT
        TO_CHAR(order_date, 'YYYY-MM') AS sales_month,
        ROUND(SUM(revenue), 2) AS total_revenue,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        COUNT(DISTINCT customer_id) AS active_customers,
        ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value
    FROM RETAIL_DWH.STAGING_LAYER.STG_RETAIL_SALES
    GROUP BY TO_CHAR(order_date, 'YYYY-MM')
)
SELECT
    sales_month,
    total_revenue,
    total_orders,
    total_units_sold,
    active_customers,
    avg_order_value,
    ROUND(total_revenue - LAG(total_revenue, 1, total_revenue) OVER (ORDER BY sales_month), 2) AS mom_revenue_growth
FROM monthly
ORDER BY sales_month ASC;

-- Step 7: Configure Transformer Role & Permissions
USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE ROLE RETAIL_TRANSFORMER_ROLE;
GRANT USAGE ON WAREHOUSE RETAIL_WH TO ROLE RETAIL_TRANSFORMER_ROLE;
GRANT ALL PRIVILEGES ON DATABASE RETAIL_DWH TO ROLE RETAIL_TRANSFORMER_ROLE;
GRANT ALL PRIVILEGES ON ALL SCHEMAS IN DATABASE RETAIL_DWH TO ROLE RETAIL_TRANSFORMER_ROLE;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN DATABASE RETAIL_DWH TO ROLE RETAIL_TRANSFORMER_ROLE;
