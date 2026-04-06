-- 生產線產量對比 (按月)
SELECT
    d.year,
    d.month_name,
    m.line_no,
    SUM(f.actual_quantity) AS total_output
FROM olap.fact_production f
JOIN olap.dim_date d ON f.date_key = d.date_key
JOIN olap.dim_machines m ON f.machine_key = m.machine_key
GROUP BY d.year, d.month_name, m.line_no
ORDER BY d.year DESC, total_output DESC;


-- 設備稼動率分析 (OEE 基礎指標)
-- 對於極高頻的 Dashboard，可以建立 Materialized View
SELECT
    m.machine_name,
    SUM(CASE WHEN f.status = 'Running' THEN f.duration_seconds ELSE 0 END) * 100.0 /
    SUM(f.duration_seconds) AS availability_rate
FROM olap.fact_machine_activity f
JOIN olap.dim_machines m ON f.machine_key = m.machine_key
WHERE f.start_time >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY m.machine_name;


-- 產品生產效率排行 (Top 5 產品)
SELECT
    p.product_name,
    m.machine_name,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.actual_quantity) AS total_quantity
FROM olap.fact_production f
JOIN olap.dim_products p ON f.product_key = p.product_key
JOIN olap.dim_machines m ON f.machine_key = m.machine_key
GROUP BY p.product_name, m.machine_name
ORDER BY total_quantity DESC
LIMIT 5;