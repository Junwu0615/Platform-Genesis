INSERT INTO olap.dim_machine (machine_id, machine_name, machine_type, line_no)
SELECT machine_id, machine_name, machine_type, line_no
FROM oltp.machine
ON CONFLICT (machine_id) DO UPDATE SET
    machine_name = EXCLUDED.machine_name,
    line_no = EXCLUDED.line_no;