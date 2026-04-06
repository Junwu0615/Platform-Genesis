INSERT INTO olap.dim_machine (machine_id, machine_name,
                              machine_type, line_no)
SELECT machine_id, machine_name, machine_type, line_no
FROM oltp.machine
ON CONFLICT (machine_id) -- 指定衝突的欄位（必須 UNIQUE 索引）
DO UPDATE SET            -- 如果衝突發生，執行更新
    machine_name = EXCLUDED.machine_name,
    machine_type = EXCLUDED.machine_type,
    line_no = EXCLUDED.line_no,
    updated_at = CURRENT_TIMESTAMP
;