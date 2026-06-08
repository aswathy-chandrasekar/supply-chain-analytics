-- ════════════════════════════════════════════════════════
-- SUPPLY CHAIN ANALYTICS — CORE SQL QUERIES
-- ════════════════════════════════════════════════════════

-- ── 1. OVERALL LATE DELIVERY RATE ───────────────────────
SELECT
    ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_delivery_pct,
    COUNT(*) AS total_orders,
    SUM(is_late) AS late_orders
FROM orders;

-- ── 2. LATE DELIVERY RATE BY SHIPPING MODE ──────────────
SELECT
    shipping_mode,
    COUNT(*) AS total_orders,
    SUM(is_late) AS late_orders,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_pct,
    ROUND(AVG(days_for_shipping_real), 1) AS avg_actual_days,
    ROUND(AVG(days_for_shipment_scheduled), 1) AS avg_scheduled_days
FROM orders
GROUP BY shipping_mode
ORDER BY late_pct DESC;

-- ── 3. LATE DELIVERY RATE BY MARKET ─────────────────────
SELECT
    market,
    COUNT(*) AS total_orders,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_pct,
    ROUND(AVG(order_profit_per_order), 2) AS avg_profit
FROM orders
GROUP BY market
ORDER BY late_pct DESC;

-- ── 4. TOP 10 MOST PROFITABLE PRODUCT CATEGORIES ────────
SELECT
    category_name,
    COUNT(*) AS total_orders,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(AVG(order_profit_per_order), 2) AS avg_profit,
    ROUND(AVG(order_item_discount_rate) * 100, 2) AS avg_discount_pct
FROM orders
GROUP BY category_name
ORDER BY total_profit DESC
LIMIT 10;

-- ── 5. MONTHLY REVENUE & PROFIT TREND ───────────────────
SELECT
    order_year,
    order_month,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(100.0 * SUM(order_profit_per_order) / SUM(sales), 2) AS profit_margin_pct
FROM orders
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

-- ── 6. CUSTOMER SEGMENT PERFORMANCE ─────────────────────
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(AVG(sales_per_customer), 2) AS avg_sales_per_customer,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_delivery_pct
FROM orders
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- ── 7. SHIPPING MODE vs PROFIT IMPACT ───────────────────
SELECT
    shipping_mode,
    customer_segment,
    COUNT(*) AS orders,
    ROUND(AVG(order_profit_per_order), 2) AS avg_profit,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_pct
FROM orders
GROUP BY shipping_mode, customer_segment
ORDER BY shipping_mode, avg_profit DESC;

-- ── 8. DEPARTMENT REVENUE BREAKDOWN ─────────────────────
SELECT
    department_name,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(order_profit_per_order), 2) AS total_profit,
    ROUND(100.0 * SUM(order_profit_per_order) / SUM(sales), 2) AS profit_margin_pct
FROM orders
GROUP BY department_name
ORDER BY total_revenue DESC;

-- ── 9. ORDER STATUS BREAKDOWN ───────────────────────────
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total,
    ROUND(SUM(sales), 2) AS total_revenue
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- ── 10. HIGH RISK LATE DELIVERY SEGMENTS (for dashboard)─
SELECT
    market,
    shipping_mode,
    customer_segment,
    COUNT(*) AS total_orders,
    ROUND(100.0 * SUM(is_late) / COUNT(*), 2) AS late_pct,
    ROUND(AVG(order_profit_per_order), 2) AS avg_profit
FROM orders
GROUP BY market, shipping_mode, customer_segment
HAVING COUNT(*) > 100
ORDER BY late_pct DESC
LIMIT 20;