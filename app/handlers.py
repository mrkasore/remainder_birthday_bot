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

class EditBirthdayState(StatesGroup):
    waiting_for_fio = State()
    waiting_for_date = State()

class EditCallbackData(CallbackData, prefix="edit"):
    record_id: int

class DeleteCallbackData(CallbackData, prefix="delete"):
    record_id: int

@router.message(CommandStart())
async def cmd_start(message: Message):
    await db.create_user(message.from_user.full_name, message.from_user.id)
    await message.answer(f'Привет, {str(message.from_user.full_name)}!', reply_markup = kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(
        "👋 Привет! Я бот для управления днями рождения.\n\n"
        "Вот список доступных команд:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить справочную информацию\n"
    )

@router.message(F.text == 'Добавить дату')
async def add_birthday_event(message: Message, state: FSMContext):
    await state.set_state(AddDate.fio)
    await message.answer('Введите ФИО:')

@router.message(AddDate.fio)
async def add_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(AddDate.date)
    await message.answer('Введите дату роджения (ГГГГ-ММ-ДД)')

@router.message(AddDate.date)
async def add_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    user_id = await db.get_user_id(message.from_user.id)
    if user_id:
        await db.add_birthday_db(data["fio"], data["date"], user_id, message.from_user.id)
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
async def edit_birthday_callback(callback_query: CallbackQuery, callback_data: EditCallbackData, state: FSMContext):
    record_id = callback_data.record_id
    record = await db.get_birthday(record_id)
    res_message = await get_current_birthday_row(record)
    await callback_query.message.answer(f"Редактируем запись:\n{res_message}", reply_markup=kb.choose_edit)
    await callback_query.answer()
    await state.update_data(record_id=record_id)

@router.callback_query(F.data == 'change_fio')
async def change_fio(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите новое ФИО')
    await state.set_state(EditBirthdayState.waiting_for_fio)
    await callback.answer()

@router.callback_query(F.data == 'change_date')
async def change_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите новую дату (ГГГГ-ММ-ДД)')
    await state.set_state(EditBirthdayState.waiting_for_date)
    await callback.answer()

@router.message(EditBirthdayState.waiting_for_fio)
async def process_new_fio(message: Message, state: FSMContext):
    new_fio = message.text
    data = await state.get_data()
    await db.update_data(data['record_id'], new_fio, 'fio', message.from_user.id)
    await message.answer(f'Поле ФИО изменено на {new_fio}')
    await state.clear()

@router.message(EditBirthdayState.waiting_for_date)
async def process_new_fio(message: Message, state: FSMContext):
    new_date = message.text
    data = await state.get_data()
    await db.update_data(data['record_id'], new_date, 'date', message.from_user.id)
    await message.answer(f'Поле даты изменено на {new_date}')
    await state.clear()

@router.callback_query(DeleteCallbackData.filter())
async def delete_birthday_callback(callback_query: CallbackQuery, callback_data: DeleteCallbackData):
    record_id = callback_data.record_id
    try:
        await db.delete_date(record_id)
        await callback_query.message.answer(f'Запись удалена ID - {record_id}')
        await callback_query.answer()
    except:
        await callback_query.message.answer(f'Запись ID - {record_id} уже была удалена ранее')

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
