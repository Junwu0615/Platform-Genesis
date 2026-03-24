CREATE TABLE oltp.production_orders (
    order_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES oltp.products(product_id),
    planned_quantity INT,
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_orders_product
ON oltp.production_orders(product_id);