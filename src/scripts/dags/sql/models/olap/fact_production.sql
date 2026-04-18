SET ROLE olap_owner;

CREATE TABLE olap.fact_production (
    fact_id BIGSERIAL NOT NULL,
    date_key INT REFERENCES olap.dim_date(date_key),
    machine_key INT REFERENCES olap.dim_machine(machine_key),
    product_key INT REFERENCES olap.dim_product(product_key),
    order_id INT,
    quantity INT,
    is_completed BOOLEAN, -- 用於計算進度的指標
    event_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_fact_production PRIMARY KEY (fact_id, event_timestamp) -- 必須包含 event_timestamp 才能建立 PK
) PARTITION BY RANGE (event_timestamp);


-- 順序決定了索引的生死 ( 關於匹配原則無法跳過，否則失效成代價極高的 Full Scan )
CREATE INDEX idx_olap_prod_composite
ON olap.fact_production(machine_key);


-- 防止萬一的保險：任何不在範圍內的資料都會掉進這裡
CREATE TABLE olap.fact_production_default
PARTITION OF olap.fact_production DEFAULT;

RESET ROLE;