import sqlite3

DB_NAME = "krishi.db"

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Farmers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS farmers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        location TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Admin table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Insert default admin (only once)
    cur.execute("SELECT COUNT(*) FROM admins")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()
