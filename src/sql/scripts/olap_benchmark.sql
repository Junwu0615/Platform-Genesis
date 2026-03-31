SELECT machine_id, COUNT(*), AVG(quantity)
FROM oltp.production_records
WHERE 1=1
AND event_time >= '2026-03-01'
GROUP BY machine_id
ORDER BY machine_id ASC
;