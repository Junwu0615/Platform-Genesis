SET ROLE oltp_owner;

CREATE TABLE oltp.machine_events (
    event_id BIGSERIAL PRIMARY KEY,
    machine_id INT REFERENCES oltp.machine(machine_id),
    event_type VARCHAR(50),
    description TEXT,
    event_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_events_machine_time
ON oltp.machine_events(machine_id, event_time);

RESET ROLE;