/*
    Analytics Mart: fct_sales_monthly
    Aggregates retail transactions on a monthly cadence to track growth and seasonality.
    Directly answers Business Question 3:
    "How does revenue change month by month?"
*/

WITH sales AS (
    SELECT * FROM retail_staging.stg_retail_sales
),

monthly_aggregates AS (
    SELECT
        STRFTIME(order_date, '%Y-%m') AS sales_month,
        ROUND(SUM(revenue), 2) AS total_revenue,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_units_sold,
        COUNT(DISTINCT customer_id) AS active_customers,
        ROUND(AVG(revenue), 2) AS avg_order_value
    FROM sales
    GROUP BY STRFTIME(order_date, '%Y-%m')
)

SELECT
    sales_month,
    total_revenue,
    total_orders,
    total_units_sold,
    active_customers,
    avg_order_value,
    ROUND(total_revenue - LAG(total_revenue, 1, total_revenue) OVER (ORDER BY sales_month), 2) AS mom_revenue_growth
FROM monthly_aggregates
ORDER BY sales_month ASC
