from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "tnved.db"

print("TNVED DB:", DB_PATH.resolve())   # <-- добавить

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():
    conn = get_connection()
#    conn.execute("""
 #       DROP TABLE IF EXISTS tnved
  #  """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tnved
        (
            code TEXT PRIMARY KEY,

            description TEXT NOT NULL,

            duty_text TEXT,

            calculation_type INTEGER NOT NULL,

            percent_rate REAL,

            specific_rate REAL,

            specific_currency TEXT,

            specific_unit TEXT,

            specific_quantity REAL,

            vat REAL,

            details TEXT,

            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_tnved_description
        ON tnved(description);
    """)

    conn.commit()
    conn.close()