import logging

from flask import Flask

from .config import get_db_config
from .connection import get_connection

logger = logging.getLogger(__name__)


def init_db(app: Flask):
    config = get_db_config()
    
    if "jdbc_url" not in config:
        if not all([config.get("database"), config.get("user"), config.get("password")]):
            raise ValueError("Missing database environment variables: DB_NAME, DB_USER, DB_PASSWORD")
    
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        logger.info("Database connection test successful")
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise ConnectionError(f"Failed to connect to database: {e}") from e
    finally:
        if conn:
            conn.close()
    
    return config
