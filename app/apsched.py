from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.bot import bot
import app.gpt as gpt_yandex

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

async def send_scheduled_message(user_id, message_text, about_user, is_male):
    await bot.send_message(user_id, message_text)
    congratulations_text = await gpt_yandex.get_text_from_gpt(about_user, is_male)
    await bot.send_message(user_id, "Предлагаю данный вариант для поздравления 😉")
    await bot.send_message(user_id, congratulations_text)


async def load_task(id_birthday, user_id, message, day, month, about_user, is_male):
    scheduler.add_job(
        send_scheduled_message,
        "cron",
        day=day,
        month=month,
        hour=18,
        minute=12,
        args=[user_id, message, about_user, is_male],
        id=str(id_birthday),
        replace_existing=True,
    )

async def send_data_to_schedule(birthday_date, birthday_id, fio, user_id, about_user, is_male):
    year, month, day = birthday_date.split('-')
    message = f'Поздравь с Днем Рождения {fio}'
    await load_task(birthday_id, user_id,  message, day, month, about_user, is_male)

async def modify_schedule_job(record_id, new_variable, column):
    job = scheduler.get_job(job_id=str(record_id))

    if column == 'fio':
        message = f'Поздравь с Днем Рождения {new_variable}'
        if job:
            current_args = list(job.args)
            current_args[1] = message

            scheduler.modify_job(
                job_id=str(record_id),
                args=current_args,
            )
    elif column == 'about_user':
        if job:
            current_args = list(job.args)
            current_args[2] = new_variable

            scheduler.modify_job(
                job_id=str(record_id),
                args=current_args,
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
    try:
        scheduler.remove_job(str(job_id))
    except:
        return False