import asyncio
import os
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
import logging

from app.handlers import router
from app import database as db

load_dotenv()

dp = Dispatcher()
token = os.getenv('TOKEN')
bot = Bot(token=token)

async def on_startup():
    await db.db_start()

async def main():
    logging.basicConfig(level=logging.INFO)
    await db.db_start()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())