from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!', reply_markup= kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Помощь')