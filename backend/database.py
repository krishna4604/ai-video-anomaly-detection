import sqlite3

DB = "data/logs.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score REAL,
        label TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_log(score, label):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO logs (score, label) VALUES (?, ?)", (score, label))

    conn.commit()
    conn.close()