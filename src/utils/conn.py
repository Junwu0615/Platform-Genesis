# -*- coding: utf-8 -*-
import psycopg2

MODULE_NAME = __name__.upper()

def get_conn(db, logging) -> psycopg2.extensions.connection:
    while True:
        try:
            conn = psycopg2.connect(**db)
            conn.autocommit = False
            return conn
        except Exception as e:
            logging.error('Connect Failed Retrying...', exc_info=True)
            time.sleep(3)


def close_conn(conn, cursor, logging):
    if cursor:
        cursor.close()
        logging.warning("'cursor.close()' called ...")
    if conn:
        conn.close()
        logging.warning("'conn.close()' called ...")