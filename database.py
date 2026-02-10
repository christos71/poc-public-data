import sqlite3

DB_NAME = "poc.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deliberations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        law_num TEXT NOT NULL,
        law_title TEXT,
        ministry TEXT,
        deliberation_title TEXT,
        deliberation_start DATE,
        deliberation_end DATE,
        source TEXT,
        last_updated TEXT
    )
    """)

    conn.commit()
    conn.close()
