"""
Update Date: 2026-03-24
"""
import psycopg2

TARGET_LIST = [
    'oltp.production_records',
    'oltp.staging_logs'
    'oltp.staging_logs'
    'oltp.staging_logs'
    'oltp.staging_logs'
    'oltp.staging_logs'
]

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

        for table in TARGET_LIST:
            sql = f"DELETE FROM {table} WHERE 1=1"
            cursor.execute(sql)
        conn.commit()

    except Exception as e:
        print('Exception:', e)

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()

if __name__ == '__main__':
    main()