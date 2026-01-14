import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g

from .config import get_db_config


def get_db_connection():
    if "db_conn" not in g:
        config = get_db_config()

        if "jdbc_url" in config:
            g.db_conn = psycopg2.connect(config["jdbc_url"], cursor_factory=RealDictCursor)
        else:
            g.db_conn = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                database=config["database"],
                user=config["user"],
                password=config["password"],
                cursor_factory=RealDictCursor,
            )

    return g.db_conn


def close_db_connection(e=None):
    db_conn = g.pop("db_conn", None)

    if db_conn is not None:
        db_conn.close()


def init_db(app):
    app.teardown_appcontext(close_db_connection)

    with app.app_context():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS credit_cards (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    last_four VARCHAR(4) NOT NULL,
                    card_type VARCHAR(50) NOT NULL,
                    expiry_month INTEGER NOT NULL,
                    expiry_year INTEGER NOT NULL,
                    cardholder_name VARCHAR(255) NOT NULL,
                    billing_address_line1 TEXT,
                    billing_address_line2 TEXT,
                    billing_city VARCHAR(100),
                    billing_state VARCHAR(100),
                    billing_postal_code VARCHAR(20),
                    billing_country VARCHAR(100),
                    payment_token TEXT,
                    is_default BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    card_id INTEGER REFERENCES credit_cards(id),
                    amount DECIMAL(10, 2) NOT NULL,
                    currency VARCHAR(3) DEFAULT 'USD',
                    status VARCHAR(50) DEFAULT 'pending',
                    processor VARCHAR(50),
                    processor_transaction_id VARCHAR(255),
                    description TEXT,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_credit_cards_user_id
                ON credit_cards(user_id);
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_transactions_user_id
                ON transactions(user_id);
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_transactions_status
                ON transactions(status);
            """)

            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Database initialization error: {e}")
