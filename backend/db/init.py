from flask import Flask

from .config import get_db_config


def init_db(app: Flask):
    config = get_db_config()
    if not all([config["database"], config["user"], config["password"]]):
        raise ValueError("Missing database environment variables: DB_NAME, DB_USER, DB_PASSWORD")
    return config
