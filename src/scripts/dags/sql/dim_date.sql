INSERT INTO olap.dim_date (
    date_key,
    date,
    day_of_week,
    is_weekend,
    month_name,
    year,
    quarter
)
SELECT
    to_char(datum, 'YYYYMMDD')::INT AS date_key,
    datum AS date,
    EXTRACT(ISODOW FROM datum) AS day_of_week, -- 1 (週一) 到 7 (週日)
    CASE WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend,
    trim(to_char(datum, 'Month')) AS month_name,
    EXTRACT(YEAR FROM datum) AS year,
    EXTRACT(QUARTER FROM datum) AS quarter
FROM generate_series(
    '2025-01-01'::DATE,
    '2030-12-31'::DATE,
    '1 day'::INTERVAL
) AS datum
ON CONFLICT (date_key) DO NOTHING; -- 避免重複執行報錯