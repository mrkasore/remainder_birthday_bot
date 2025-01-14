import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()
token = os.getenv('TOKEN')
bot = Bot(token=token)