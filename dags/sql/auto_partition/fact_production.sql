DO $$
DECLARE
    target_schema TEXT := 'olap';
    target_table  TEXT := 'fact_production';

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

        BEGIN
            SET ROLE olap_owner;
            EXECUTE format(
                'CREATE TABLE IF NOT EXISTS %I.%I
                PARTITION OF %I.%I
                FOR VALUES FROM (%L) TO (%L)',
                target_schema, partition_name,
                target_schema, target_table,
                start_date, end_date
            );

            RAISE NOTICE '成功檢查/建立分區: %.%', target_schema, partition_name;

        EXCEPTION
            WHEN invalid_object_definition THEN
                RAISE WARNING '跳過分區 %.%: 範圍 [% 到 %] 與現有分區重疊',
                              target_schema, partition_name, start_date, end_date;

            WHEN duplicate_table THEN
                RAISE NOTICE '分區 %.% 已存在，跳過。', target_schema, partition_name;

            WHEN OTHERS THEN
                RAISE WARNING '建立分區 %.% 時發生未知錯誤: %', target_schema, partition_name, SQLERRM;
        END;

    END LOOP;
    RESET ROLE;

END $$;