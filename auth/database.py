from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "users.db"


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

def initialize_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            name TEXT NOT NULL,

            email TEXT,

            role TEXT NOT NULL,

            active INTEGER NOT NULL DEFAULT 1,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            last_login TEXT
        )        
    """)

    conn.commit()
    conn.close()

def initialize_sessions():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions
        (
            token TEXT PRIMARY KEY,

            user_id INTEGER NOT NULL,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            expires_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()