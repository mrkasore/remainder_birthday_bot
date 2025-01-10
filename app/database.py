import sqlite3 as sq

db = sq.connect('database.db')
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "name TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS birthdays ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "fio TEXT,"
                "date DATE,"
                "user_id INTEGER,"
                "FOREIGN KEY (user_id) REFERENCES users (id))")

    db.commit()

