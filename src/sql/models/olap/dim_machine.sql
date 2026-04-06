CREATE TABLE olap.dim_machine (
    machine_key SERIAL PRIMARY KEY,
    machine_id INT NOT NULL CONSTRAINT uq_dim_machine_name UNIQUE,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(50) NOT NULL,
    line_no VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT Null
);


CREATE INDEX idx_dim_machine_id
ON olap.dim_machine(machine_id);