SET ROLE oltp_owner;

CREATE TABLE oltp.product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_type VARCHAR(50),
    target_qty INT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT Null
);

RESET ROLE;