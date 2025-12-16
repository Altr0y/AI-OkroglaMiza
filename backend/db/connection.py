import psycopg2
from psycopg2.extras import RealDictCursor

from .config import get_db_config


def get_connection():
    config = get_db_config()
    return psycopg2.connect(
        host=config["host"],
        port=config["port"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
    )


def execute_query(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        conn.close()


def execute_command(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
