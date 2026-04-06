DO $$
DECLARE
    target_schema TEXT := 'oltp';
    target_table  TEXT := 'production_records';

    run_date      DATE;
    start_date    DATE;
    end_date      DATE;
    partition_name TEXT;
BEGIN
    -- 迴圈建立分區表
    FOR i IN 0..3 LOOP
        run_date   := date_trunc('day', CURRENT_DATE + (i || ' day')::interval);
        start_date := run_date;
        end_date   := run_date + interval '1 day';
        partition_name := target_table || '_' || to_char(start_date, 'YYYY_MM_DD');

        EXECUTE format(
            'SET ROLE oltp_owner;
            CREATE TABLE IF NOT EXISTS %I.%I
            PARTITION OF %I.%I
            FOR VALUES FROM (%L) TO (%L)',
            target_schema, partition_name,
            target_schema, target_table,
            start_date, end_date
        );

        RAISE NOTICE '檢查並確保分區存在: %.%', target_schema, partition_name;

    END LOOP;
END $$;