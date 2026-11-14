/*
    Analytics Mart: dim_products_sales
    Aggregates retail transactions by product and category.
    Directly answers Business Question 1:
    "Which product generated the highest revenue?"
*/

WITH sales AS (
    SELECT * FROM retail_staging.stg_retail_sales
),

product_metrics AS (
    SELECT
        product_name,
        category,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        ROUND(SUM(revenue), 2) AS total_revenue,
        ROUND(SUM(CASE WHEN payment_status = 'Completed' THEN revenue ELSE 0 END), 2) AS completed_revenue,
        ROUND(AVG(unit_price), 2) AS avg_unit_price
    FROM sales
    GROUP BY product_name, category
)

SELECT
    product_name,
    category,
    total_orders,
    total_units_sold,
    total_revenue,
    completed_revenue,
    avg_unit_price,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM product_metrics
ORDER BY total_revenue DESC
