-- 1. Repeat Purchase Baseline
SELECT 
    COUNT(DISTINCT customer_unique_id) AS total_unique_customers,
    COUNT(DISTINCT CASE WHEN order_count > 1 THEN customer_unique_id END) AS repeat_customers,
    ROUND(
        (COUNT(DISTINCT CASE WHEN order_count > 1 THEN customer_unique_id END) * 100.0) / 
        COUNT(DISTINCT customer_unique_id), 
        2
    ) AS repeat_purchase_rate_pct
FROM (
    SELECT 
        c.customer_unique_id,
        COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
);

-- 2. Delivery Timeliness vs Review Score
SELECT 
    CASE 
        WHEN DATE(o.order_delivered_customer_date) <= DATE(o.order_estimated_delivery_date) THEN 'On-Time / Early'
        ELSE 'Late'
    END AS delivery_performance,
    COUNT(o.order_id) AS total_orders,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2) AS avg_review_score,
    ROUND(
        (COUNT(CASE WHEN CAST(r.review_score AS INT) = 1 THEN 1 END) * 100.0) / COUNT(o.order_id), 
        2
    ) AS pct_one_star_reviews
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY delivery_performance;

-- 3. Top Churn Categories
SELECT 
    COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS category_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(AVG(CAST(r.review_score AS FLOAT)), 2) AS avg_review_score,
    COUNT(CASE WHEN CAST(r.review_score AS INT) = 1 THEN 1 END) AS count_1_star_reviews,
    ROUND(
        (COUNT(CASE WHEN CAST(r.review_score AS INT) = 1 THEN 1 END) * 100.0) / COUNT(o.order_id), 
        2
    ) AS pct_1_star_reviews
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t 
    ON p.product_category_name = t."﻿product_category_name"
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY category_name
HAVING total_orders >= 500
ORDER BY pct_1_star_reviews DESC
LIMIT 10;
