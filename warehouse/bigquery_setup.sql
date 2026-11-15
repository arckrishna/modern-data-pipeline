-- =============================================================================
-- RETAILPULSE AI: TARGET DATA WAREHOUSE DDL (GOOGLE BIGQUERY)
-- =============================================================================
-- Subject: Data Engineering Microproject
-- Target: Google Cloud BigQuery (Free Tier / Sandbox / Student Account)
-- Architecture: Medallion Architecture (retail_raw -> retail_staging -> retail_analytics)
-- =============================================================================

-- Step 1: Create Datasets for Each Medallion Tier
CREATE SCHEMA IF NOT EXISTS `retail_raw`
OPTIONS (location = "US", description = "Bronze tier: Raw ingested sales transactions from Airbyte");

CREATE SCHEMA IF NOT EXISTS `retail_staging`
OPTIONS (location = "US", description = "Silver tier: Cleaned, standardized, and typed views built by dbt");

CREATE SCHEMA IF NOT EXISTS `retail_analytics`
OPTIONS (location = "US", description = "Gold tier: Aggregated business marts powering RetailPulse AI Conversational BI");

-- =============================================================================
-- STEP 2: BRONZE TIER (RAW LANDING TABLE)
-- =============================================================================
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
OPTIONS (description = "Raw ingested retail sales transactions");

-- =============================================================================
-- STEP 3: SILVER TIER (STAGING CLEANED VIEW)
-- =============================================================================
CREATE OR REPLACE VIEW `retail_staging.stg_retail_sales` AS
SELECT
    TRIM(order_id) AS order_id,
    PARSE_DATE('%Y-%m-%d', order_date) AS order_date,
    TRIM(customer_id) AS customer_id,
    TRIM(product) AS product_name,
    TRIM(category) AS category,
    TRIM(region) AS region,
    CAST(quantity AS INT64) AS quantity,
    CAST(unit_price AS NUMERIC) AS unit_price,
    ROUND(CAST(quantity AS INT64) * CAST(unit_price AS NUMERIC), 2) AS revenue,
    TRIM(payment_status) AS payment_status,
    _ingested_at
FROM `retail_raw.raw_retail_sales`
WHERE order_id IS NOT NULL
  AND CAST(quantity AS INT64) > 0
  AND CAST(unit_price AS NUMERIC) > 0;

-- =============================================================================
-- STEP 4: GOLD TIER (ANALYTICS MARTS)
-- =============================================================================

-- Mart 1: Product Revenue & Ranking (Answers Business Question 1)
CREATE OR REPLACE TABLE `retail_analytics.dim_products_sales` AS
SELECT
    product_name,
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN payment_status = 'Completed' THEN revenue ELSE 0 END), 2) AS completed_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS revenue_rank
FROM `retail_staging.stg_retail_sales`
GROUP BY product_name, category
ORDER BY total_revenue DESC;

-- Mart 2: Regional Performance & AOV (Answers Business Question 2)
CREATE OR REPLACE TABLE `retail_analytics.dim_regional_performance` AS
SELECT
    region,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value,
    ROUND(SUM(CASE WHEN payment_status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS completion_rate_pct,
    RANK() OVER (ORDER BY SUM(revenue) DESC) AS regional_rank
FROM `retail_staging.stg_retail_sales`
GROUP BY region
ORDER BY total_revenue DESC;

-- Mart 3: Monthly Fact Trends & MoM Growth (Answers Business Question 3)
CREATE OR REPLACE TABLE `retail_analytics.fct_sales_monthly` AS
WITH monthly AS (
    SELECT
        FORMAT_DATE('%Y-%m', order_date) AS sales_month,
        ROUND(SUM(revenue), 2) AS total_revenue,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        COUNT(DISTINCT customer_id) AS active_customers,
        ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS avg_order_value
    FROM `retail_staging.stg_retail_sales`
    GROUP BY FORMAT_DATE('%Y-%m', order_date)
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
