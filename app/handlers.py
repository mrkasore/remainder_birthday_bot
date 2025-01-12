from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database as db

router = Router()

class AddDate(StatesGroup):
    fio = State()
    date = State()

class EditCallbackData(CallbackData, prefix="edit"):
    record_id: int

@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.create_user(message.from_user.full_name, message.from_user.id)
    await message.answer('Привет!', reply_markup = kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Помощь')

@router.message(F.text == 'Добавить дату')
async def add_birthday_event(message: Message, state: FSMContext):
    await state.set_state(AddDate.fio)
    await message.answer('Введите ФИО:')

@router.message(AddDate.fio)
async def add_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(AddDate.date)
    await message.answer('Введите дату роджения')

@router.message(AddDate.date)
async def add_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    user_id = await db.get_user_id(message.from_user.id)
    if user_id:
        await db.add_birthday_db(data["fio"], data["date"], user_id)
        await message.answer(f'ФИО: {data["fio"]}\n'
        f'Дата Рождения: {data["date"]}')
    await state.clear()

@router.message(F.text == 'Просмотреть все даты')
async def get_all_birthdays(message: Message):
    all_birthdays = await db.get_all_dates(message.from_user.id)

    for birthday in all_birthdays:
        res_row = await get_current_birthday_row(birthday)
        await message.answer(res_row, reply_markup = kb.generate_edit_keyboard(birthday['id']))

@router.callback_query(EditCallbackData.filter())
async def edit_birthday_callback(callback_query: CallbackQuery, callback_data: EditCallbackData):
    record_id = callback_data.record_id
    record = await db.get_birthday(record_id)
    res_message = await get_current_birthday_row(record)
    await callback_query.message.answer(f"Редактируем запись:\n{res_message}")
    await callback_query.answer()

async def get_current_birthday_row(birthday):
    all_keys = {
        'fio': 'ФИО',
        'date': 'Дата рождения',
    }
    res_row = ''

    for key, row in birthday.items():
        if key in ['id', 'user_id']:
            continue
        res_row += f'{all_keys[key]}: {str(row)}\n'

    return res_row

