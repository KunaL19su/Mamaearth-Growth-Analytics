USE mamaearth_analytics;
-- Report 1 — Total Orders, Revenue & AOV --
SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(
        p.price * o.quantity * (1 - COALESCE(o.discount_pct, 0) / 100)
    ), 2) AS total_revenue,
    
    ROUND(AVG(
        p.price * o.quantity * (1 - COALESCE(o.discount_pct, 0) / 100)
    ), 2) AS average_order_value

FROM orders o
JOIN products p
    ON o.product_id = p.product_id;
    
-- Report 2 — Total Orders, Revenue & AOV --

SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS orders_with_rating,
    COUNT(*) - COUNT(rating) AS missing_ratings
FROM orders;

-- Report 3 — Zero-Order Customers --

SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Report 4 — Same check using --

SELECT
    customer_id,
    name
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id
    FROM orders
);

-- Report 5 — City-wise Return Rate > 20% --

SELECT
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(
        SUM(o.returned) * 100.0 / COUNT(o.order_id),
        2
    ) AS return_rate_pct
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING return_rate_pct > 20
ORDER BY return_rate_pct DESC;

-- Report 6 — Top 5 Customers by Spend -- 

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            p.price * o.quantity *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ),
        2
    ) AS total_spend
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC
LIMIT 5;

-- Report 6B — Rank 3 to 5 --

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            p.price * o.quantity *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ),
        2
    ) AS total_spend
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC
LIMIT 3 OFFSET 2;

-- Report 7 — Category-wise Orders & Revenue --

SELECT
    p.category,
    COUNT(o.order_id) AS total_orders,
    ROUND(
        SUM(
            p.price * o.quantity *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ),
        2
    ) AS total_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Report 8 — Customer Names Starting with "A" --

SELECT
    customer_id,
    name,
    city
FROM customers
WHERE name LIKE 'A%'
ORDER BY name;

-- Report 9 — DISTINCT Acquisition Sources. --

SELECT DISTINCT
    acquisition_source
FROM customers
ORDER BY acquisition_source;

UPDATE customers
SET loyalty_tier =
    CASE
        WHEN city_tier = 1 THEN 'Gold'
        ELSE 'Silver'
    END
WHERE customer_id BETWEEN 'C001' AND 'C045';

SELECT
    loyalty_tier,
    COUNT(*) AS customer_count
FROM customers
GROUP BY loyalty_tier;