from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.bot import bot

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

async def send_scheduled_message(user_id, message_text):
    await bot.send_message(user_id, message_text)

async def load_task(id_birthday, user_id, message, day, month):
    scheduler.add_job(
        send_scheduled_message,
        "cron",
        day=day,
        month=month,
        hour=10,
        minute=0,
        args=[user_id, message],
        id=str(id_birthday),
        replace_existing=True,
    )

async def send_data_to_schedule(birthday_date, birthday_id, fio, user_id):
    year, month, day = birthday_date.split('-')
    message = f'Поздравь с Днем Рождения {fio}'
    await load_task(birthday_id, user_id,  message, day, month)

async def modify_schedule_job(record_id, user_id, new_variable, column):
    if column == 'fio':
        message = f'Поздравь с Днем Рождения {new_variable}'
        scheduler.modify_job(
            job_id=str(record_id),
            args=[user_id, message],
        )
    elif column == 'date':
        year, month, day = new_variable.split('-')
        trigger = CronTrigger(
            day=day,
            month=month,
            hour=10,
            minute=0
        )
        scheduler.modify_job(
            job_id=str(record_id),
            trigger=trigger
        )

async def delete_schedule_job(job_id):
    scheduler.remove_job(str(job_id))