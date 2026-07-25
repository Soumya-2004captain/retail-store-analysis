-- =================================================================
-- RETAIL STORE SALES & CUSTOMER ANALYTICS
-- Database: PostgreSQL / MySQL / Standard ANSI SQL
-- Author: Soumya
-- =================================================================

-- 1. Monthly Revenue & Total Orders
SELECT 
    YEAR(order_date) AS sales_year,
    MONTH(order_date) AS sales_month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount) AS monthly_revenue_inr,
    ROUND(AVG(total_amount), 2) AS avg_order_value_inr
FROM sales_data
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY sales_year ASC, sales_month ASC;


-- 2. Top 5 Product Categories by Revenue Contribution
SELECT 
    category_name,
    SUM(total_amount) AS category_revenue_inr,
    ROUND(
        (SUM(total_amount) * 100.0) / (SELECT SUM(total_amount) FROM sales_data), 
        2
    ) AS revenue_percentage
FROM sales_data
GROUP BY category_name
ORDER BY category_revenue_inr DESC
LIMIT 5;


-- 3. Customer RFM Segmentation (Recency, Frequency, Monetary)
WITH rfm_base AS (
    SELECT 
        customer_id,
        MAX(order_date) AS last_purchase_date,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_amount) AS total_spent
    FROM sales_data
    GROUP BY customer_id
)
SELECT 
    customer_id,
    total_orders AS frequency,
    total_spent AS monetary_value_inr,
    CASE 
        WHEN total_spent >= 50000 AND total_orders >= 5 THEN 'High-Value VIP'
        WHEN total_spent BETWEEN 15000 AND 49999 THEN 'Regular Customer'
        ELSE 'At-Risk / Low-Value'
    END AS customer_segment
FROM rfm_base
ORDER BY monetary_value_inr DESC;
