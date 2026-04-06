CREATE TABLE olap.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT NOT NULL CONSTRAINT uq_dim_product_id UNIQUE,
    product_name VARCHAR(100),
    product_type VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT Null
);


CREATE INDEX idx_dim_product_id
ON olap.dim_product(product_id);