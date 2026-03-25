CREATE TABLE oltp.machine_status_logs (
    log_id BIGSERIAL,
    machine_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    event_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (event_time);


CREATE INDEX idx_status_machine_time
ON oltp.machine_status_logs(machine_id, event_time);