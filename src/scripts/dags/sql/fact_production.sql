INSERT INTO olap.fact_production (
    date_key, machine_key, product_key, order_id, quantity, event_timestamp
)
SELECT
    to_char(r.event_time, 'YYYYMMDD')::INT, -- 轉換為 Date Key
    m.machine_key,
    p.product_key,
    r.order_id,
    r.quantity,
    r.event_time
FROM oltp.production_records r
JOIN olap.dim_machine m
    ON 1=1
    AND r.machine_id = m.machine_id
JOIN olap.dim_product p
    ON 1=1
    AND r.product_id = p.product_id
WHERE 1=1
AND r.event_time >= CURRENT_TIMESTAMP - INTERVAL '1 day';