CREATE TABLE olap.fact_production (
    production_id BIGSERIAL PRIMARY KEY,
    machine_key INT REFERENCES olap.dim_machine(machine_key),
    product_key INT REFERENCES olap.dim_product(product_key),
    time_key DATE REFERENCES olap.dim_time(time_key),
    quantity INT
);


CREATE INDEX idx_fact_production_machine_time
ON olap.fact_production(machine_key, time_key);