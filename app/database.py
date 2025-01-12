import aiosqlite

DATABASE_PATH = 'database.db'

async def db_start():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "telegram_id BIGINT,"
                "name TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS birthdays ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "fio TEXT,"
                "date DATE,"
                "user_id INTEGER,"
                "FOREIGN KEY (user_id) REFERENCES users (id))")
        await db.commit()

async def create_user(name, telegram_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute('SELECT telegram_id FROM users WHERE telegram_id = ?', (telegram_id,))
        data = await cursor.fetchone()
        if data is not None:
            return

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
        await db.commit()

async def get_user_id(telegram_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
        user_id = await cursor.fetchone()
        return user_id[0]

async def add_birthday_db(fio, date, user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO birthdays (fio, date, user_id) VALUES(?, ?, ?)", (fio, date, user_id))
        await db.commit()

async def get_all_dates(telegram_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        user_id = await get_user_id(telegram_id)
        cursor = await db.execute("SELECT * FROM birthdays WHERE user_id = ?", (user_id, ))
        rows = await cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        all_dates = [dict(zip(columns, row)) for row in rows]
        return all_dates

async def get_birthday(record_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT * FROM birthdays WHERE id = ?", (record_id, ))
        res = await cursor.fetchone()
        columns = [column[0] for column in cursor.description]
        res = dict(zip(columns, res))
        return res

