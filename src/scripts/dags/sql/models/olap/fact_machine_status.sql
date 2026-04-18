CREATE TABLE olap.fact_machine_status (
    status_id BIGSERIAL PRIMARY KEY,
    date_key INT REFERENCES olap.dim_date(date_key),
    machine_key INT REFERENCES olap.dim_machine(machine_key),
    status VARCHAR(20),
    duration_seconds INT, -- 預先計算持續時間，方便 SUM 聚合
    start_time TIMESTAMPTZ DEFAULT Null,
    end_time TIMESTAMPTZ DEFAULT Null
);


CREATE INDEX idx_fact_status_lookup
ON olap.fact_machine_status(machine_key, start_time, status);