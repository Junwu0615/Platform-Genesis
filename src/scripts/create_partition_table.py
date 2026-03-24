"""
Update Date: 2026-03-24
Description: creates partition tables for machine_status_logs based on the month of log_time
"""
import logging, psycopg2

def main():
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="pgdatabase",
            user="migration_user",
            password="migration_pwd"
        )
        cursor = conn.cursor()

        sql = """
        DO $$
        DECLARE
            start_time DATE;
            end_time DATE;
            schema_mode TEXT;
            table_name TEXT;
            target_name TEXT;
        BEGIN
            SET ROLE oltp_owner;
        
            schema_mode := 'oltp';
            target_name := 'machine_status_logs';
        
            start_time := date_trunc('month', CURRENT_DATE);
            end_time := start_time + interval '1 month';
            table_name := target_name || '_' || to_char(start_time, 'YYYY_MM');
        
            EXECUTE format(
                'CREATE TABLE IF NOT EXISTS %I.%I
                PARTITION OF %I.%I
                FOR VALUES FROM (%L) TO (%L)',
                schema_mode,
                table_name,
                schema_mode,
                target_name,
                start_time,
                end_time
            );
            
            RESET ROLE;
        END $$;
        """
        cursor.execute(sql)
        logging.info('[This Mon] Partition Table ...')

        sql = """
        DO $$
        DECLARE
            start_time DATE;
            end_time DATE;
            schema_mode TEXT;
            table_name TEXT;
            target_name TEXT;
        BEGIN
            SET ROLE oltp_owner;
        
            schema_mode := 'oltp';
            target_name := 'machine_status_logs';

            start_time := date_trunc('month', CURRENT_DATE + interval '1 month');
            end_time := start_time + interval '1 month';
            table_name := target_name || '_' || to_char(start_time, 'YYYY_MM');

            EXECUTE format(
                'CREATE TABLE IF NOT EXISTS %I.%I
                PARTITION OF %I.%I
                FOR VALUES FROM (%L) TO (%L)',
                schema_mode,
                table_name,
                schema_mode,
                target_name,
                start_time,
                end_time
            );

            RESET ROLE;
        END $$;
        """
        cursor.execute(sql)
        logging.info('[Next Mon] Partition Table ...')

        conn.commit()
        logging.warning("Created partition table for 'machine_status_logs' successfully.")

    except Exception as e:
        logging.error('Exception: ', exc_info=True)
        conn.rollback()

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()

if __name__ == '__main__':
    main()