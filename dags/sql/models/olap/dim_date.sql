SET ROLE olap_owner;

CREATE TABLE olap.dim_date (
    date_key INT PRIMARY KEY,
    date DATE,
    day_of_week INT,
    is_weekend BOOLEAN,
    month_name VARCHAR(10),
    year INT,
    quarter INT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT Null
);


CREATE INDEX idx_dim_date_ymd
ON olap.dim_date(year, month_name, date);

RESET ROLE;