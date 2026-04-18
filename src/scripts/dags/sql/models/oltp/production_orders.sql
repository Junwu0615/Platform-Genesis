CREATE TABLE oltp.production_orders (
    order_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES oltp.product(product_id),
    quantity INT,
    start_at TIMESTAMPTZ DEFAULT Null,
    end_at TIMESTAMPTZ DEFAULT Null,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_orders_product
ON oltp.production_orders(product_id);