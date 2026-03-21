CREATE TABLE olap.fact_machine_status (
    status_id BIGSERIAL PRIMARY KEY,
    machine_key INT REFERENCES olap.dim_machine(machine_key),
    time_key DATE REFERENCES olap.dim_time(time_key),
    status VARCHAR(20),
    status_count INT DEFAULT 1
);


CREATE INDEX idx_fact_machine_time
ON olap.fact_machine_status(machine_key, time_key);