CREATE TABLE oltp.machines (
    machine_id SERIAL PRIMARY KEY,
    machine_name VARCHAR(100) NOT NULL CONSTRAINT uq_machine_name UNIQUE,
    machine_type VARCHAR(50),
    line_no VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_machines_line
ON oltp.machines(line_no);