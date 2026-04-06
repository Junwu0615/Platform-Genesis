DO $$
DECLARE
    target_schema TEXT := 'oltp';
    target_table  TEXT := 'machine_status_logs';

    run_date      DATE;
    start_date    DATE;
    end_date      DATE;
    partition_name TEXT;
BEGIN
    -- 迴圈建立「本月」與「下個月」的分區 (預建機制)
    FOR i IN 0..1 LOOP
        run_date   := date_trunc('month', CURRENT_DATE + (i || ' month')::interval);
        start_date := run_date;
        end_date   := run_date + interval '1 month';
        partition_name := target_table || '_' || to_char(start_date, 'YYYY_MM');

        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I.%I
            PARTITION OF %I.%I
            FOR VALUES FROM (%L) TO (%L)',
            target_schema, partition_name,
            target_schema, target_table,
            start_date, end_date
        );

        RAISE NOTICE '檢查並確保分區存在: %.%', target_schema, partition_name;

    END LOOP;
END $$;