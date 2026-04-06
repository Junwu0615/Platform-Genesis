INSERT INTO olap.dim_product (product_id, product_name, product_type)
SELECT product_id, product_name, product_type
FROM oltp.product
ON CONFLICT (product_id)
DO UPDATE SET
    product_name = EXCLUDED.product_name,
    product_type = EXCLUDED.product_type,
    updated_at = CURRENT_TIMESTAMP
;