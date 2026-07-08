import sqlite3

DATABASE="database.db"

def connect():
    return sqlite3.connect(DATABASE)

def create_tables():
    con=connect()
    cur=con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cur.execute("""
        INSERT OR IGNORE INTO users(username,password)
        VALUES('admin','admin123')
    """)

    con.commit()
    con.close()

def login(username,password):
    con=connect()
    cur=con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )
    user=cur.fetchone()
    con.close()
    return user
