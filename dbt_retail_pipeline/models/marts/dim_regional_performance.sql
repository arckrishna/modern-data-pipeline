/*
    Analytics Mart: dim_regional_performance
    Aggregates retail transactions by geographical sales region.
    Directly answers Business Question 2:
    "Which region records the highest sales performance?"
*/

WITH sales AS (
    SELECT * FROM retail_staging.stg_retail_sales
),

regional_metrics AS (
    SELECT
        region,
        ROUND(SUM(revenue), 2) AS total_revenue,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(quantity) AS total_units_sold,
        ROUND(AVG(revenue), 2) AS avg_order_value,
        ROUND(SUM(CASE WHEN payment_status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS completion_rate_pct
    FROM sales
    GROUP BY region
)

SELECT
    region,
    total_revenue,
    total_orders,
    unique_customers,
    total_units_sold,
    avg_order_value,
    completion_rate_pct,
    RANK() OVER (ORDER BY total_revenue DESC) AS regional_rank
FROM regional_metrics
ORDER BY total_revenue DESC
