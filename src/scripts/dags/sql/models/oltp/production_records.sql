CREATE TABLE oltp.production_records (
    record_id BIGSERIAL, -- 不設 PK 追求寫入速度最快
    order_id INT REFERENCES oltp.production_orders(order_id),
    machine_id INT REFERENCES oltp.machine(machine_id),
    product_id INT REFERENCES oltp.product(product_id),
    quantity INT,
    event_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (event_time);


CREATE INDEX idx_production_machine_time
ON oltp.production_records(machine_id, event_time);


-- 防止萬一的保險：任何不在範圍內的資料都會掉進這裡
CREATE TABLE oltp.production_records_default
PARTITION OF oltp.production_records DEFAULT;