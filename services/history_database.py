from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "history.db"

print("HISTORY DB:", DB_PATH.resolve())


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS calculation_history
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            calculation_name TEXT,

            product_name TEXT,
            tnved TEXT,

            qty INTEGER,
            weight REAL,
            volume REAL,
            invoice_usd REAL,

            usd_rub REAL,
            cny_rub REAL,

            full_cost REAL,
            total_customs REAL,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            cargo_json TEXT NOT NULL,
            calc_json TEXT NOT NULL,
            tariffs_json TEXT,
            rates_json TEXT,
            customs_json TEXT
        );
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_history_user_id
        ON calculation_history(user_id);
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_history_created_at
        ON calculation_history(created_at);
    """)

    conn.commit()
    conn.close()