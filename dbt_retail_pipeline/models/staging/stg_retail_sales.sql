/*
    Staging Model: stg_retail_sales
    Transforms raw retail ingestion table into clean, typed, and validated records.
    - Casts timestamps and numeric metrics
    - Standardizes categorical values
    - Calculates total revenue = quantity * unit_price
    - Filters out corrupted or non-positive records
*/

WITH source_data AS (
    SELECT
        TRIM(order_id) AS order_id,
        CAST(order_date AS DATE) AS order_date,
        TRIM(customer_id) AS customer_id,
        TRIM(product) AS product_name,
        TRIM(category) AS category,
        TRIM(region) AS region,
        CAST(quantity AS INTEGER) AS quantity,
        CAST(unit_price AS DECIMAL(10, 2)) AS unit_price,
        TRIM(payment_status) AS payment_status,
        _ingested_at
    FROM retail_raw.raw_retail_sales
),

cleaned_data AS (
    SELECT
        order_id,
        order_date,
        customer_id,
        product_name,
        category,
        region,
        quantity,
        unit_price,
        ROUND(quantity * unit_price, 2) AS revenue,
        payment_status,
        _ingested_at
    FROM source_data
    WHERE order_id IS NOT NULL
      AND quantity > 0
      AND unit_price > 0
)

SELECT * FROM cleaned_data
