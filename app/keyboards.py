from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Добавить дату', callback_data='birthday_data')],
        [KeyboardButton(text='Просмотреть все даты', callback_data='watch_all')]
    ],
    resize_keyboard=True
)