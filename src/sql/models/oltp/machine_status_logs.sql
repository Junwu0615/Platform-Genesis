CREATE TABLE oltp.machine_status_logs (
    log_id BIGSERIAL, -- 不設 PK 追求寫入速度最快
    machine_id INT REFERENCES oltp.machine(machine_id),
    status VARCHAR(20) NOT NULL,
    event_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (event_time);


CREATE INDEX idx_status_machine_time
ON oltp.machine_status_logs(machine_id, event_time);