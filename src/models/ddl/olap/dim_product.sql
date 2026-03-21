CREATE TABLE olap.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(100),
    product_type VARCHAR(50),
    created_at TIMESTAMP
);


CREATE INDEX idx_dim_product_id
ON olap.dim_product(product_id);