import os


def get_db_config():
    jdbc_url = os.getenv("DB_JDBC_URL")
    if jdbc_url:
        return {"jdbc_url": jdbc_url}
    
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
