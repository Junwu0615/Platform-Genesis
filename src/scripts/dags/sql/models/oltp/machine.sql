CREATE TABLE oltp.machine (
    machine_id SERIAL PRIMARY KEY,
    machine_name VARCHAR(100) NOT NULL CONSTRAINT uq_machine_name UNIQUE,
    machine_type VARCHAR(50),
    line_no VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT Null
);


CREATE INDEX idx_machine_line
ON oltp.machine(line_no);