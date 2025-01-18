import aiosqlite
import app.apsched as apsched

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
                "about_user TEXT,"
                "is_male BOOLEAN,"
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

async def add_birthday_db(fio, date, user_id, about_user, telegram_user_id, is_male):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("INSERT INTO birthdays (fio, date, user_id, about_user, is_male) VALUES(?, ?, ?, ?, ?)", (fio, date, user_id, about_user, is_male))
        await db.commit()
        id_birthday = cursor.lastrowid
        await apsched.send_data_to_schedule(date, id_birthday, fio, telegram_user_id, about_user, is_male)

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

async def update_data(record_id, new_variable, column):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f'UPDATE birthdays SET {column} = ? WHERE id = ?',  (new_variable, record_id, ))
        await db.commit()
        await apsched.modify_schedule_job(record_id, new_variable, column)

async def get_all_data_to_scheduler():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT birthdays.id, birthdays.fio, birthdays.date, birthdays.about_user, users.telegram_id "
                                  "FROM birthdays "
                                  "JOIN users on birthdays.user_id = users.id")

        all_dates = await cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in all_dates]

        for birthday in results:
            await apsched.send_data_to_schedule(
                birthday['date'],
                birthday['id'],
                birthday['fio'],
                birthday['telegram_id'],
                birthday['about_user'],
                birthday['is_male']
            )

        apsched.scheduler.start()

async def delete_date(record_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM birthdays WHERE id = ?", (int(record_id), ))
        await db.commit()
        await apsched.delete_schedule_job(record_id)