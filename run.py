import asyncio
from aiogram import Dispatcher
import logging

from app.handlers import router
from app import database as db
from app.bot import bot

dp = Dispatcher()

async def on_startup():
    await db.db_start()
    await db.get_all_data_to_scheduler()

async def main():
    logging.basicConfig(level=logging.INFO)
    await on_startup()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())