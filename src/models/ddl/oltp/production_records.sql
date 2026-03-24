CREATE TABLE oltp.production_records (
    record_id BIGSERIAL PRIMARY KEY,
    order_id INT REFERENCES oltp.production_orders(order_id),
    machine_id INT REFERENCES oltp.machines(machine_id),
    product_id INT REFERENCES oltp.products(product_id),
    quantity INT,
    event_time TIMESTAMPTZ NOT NULL
);


CREATE INDEX idx_production_machine_time
ON oltp.production_records(machine_id, event_time);