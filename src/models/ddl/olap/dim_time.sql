CREATE TABLE olap.dim_time (
    time_key DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT,
    hour INT,
    weekday INT,
    week INT
);


CREATE INDEX idx_dim_time_year_month
ON olap.dim_time(year, month);