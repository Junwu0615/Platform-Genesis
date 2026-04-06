INSERT INTO olap.fact_machine_status (
    date_key, machine_key, status, start_time, end_time, duration_seconds
)
WITH status_duration AS (
    SELECT
        machine_id,
        status,
        event_time AS start_time,
        LEAD(event_time) OVER (PARTITION BY machine_id ORDER BY event_time) AS end_time
    FROM oltp.machine_status_logs
    WHERE 1=1
    AND event_time >= CURRENT_TIMESTAMP - INTERVAL '1 day'
)
SELECT
    to_char(sd.start_time, 'YYYYMMDD')::INT,
    m.machine_key,
    sd.status,
    sd.start_time,
    sd.end_time,
    EXTRACT(EPOCH FROM (sd.end_time - sd.start_time))::INT -- 計算持續秒數
FROM status_duration sd
JOIN olap.dim_machine m
    ON 1=1
    AND sd.machine_id = m.machine_id
WHERE 1=1
AND sd.end_time IS NOT NULL;