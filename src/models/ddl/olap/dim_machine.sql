CREATE TABLE olap.dim_machine (
    machine_key SERIAL PRIMARY KEY,
    machine_id INT NOT NULL,
    machine_name VARCHAR(100),
    machine_type VARCHAR(50),
    line_no VARCHAR(20),
    created_at TIMESTAMP
);


CREATE INDEX idx_dim_machine_id
ON olap.dim_machine(machine_id);