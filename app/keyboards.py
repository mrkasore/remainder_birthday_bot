from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Добавить дату', callback_data='birthday_data_add')],
        [KeyboardButton(text='Просмотреть все даты', callback_data='watch_all')]
    ],
    resize_keyboard=True
)

choose_edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Изменить ФИО', callback_data='change_fio')],
        [InlineKeyboardButton(text='Изменить дату', callback_data='change_date')],
        [InlineKeyboardButton(text='Изменить информацию о человеке', callback_data='change_about_user')],
    ]
)

choose_gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='М', callback_data='male'), InlineKeyboardButton(text='Ж', callback_data='female')]
    ]
)

def generate_edit_keyboard(record_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Редактировать', callback_data=f'edit:{record_id}')],
            [InlineKeyboardButton(text='Удалить', callback_data=f'delete:{record_id}')]
        ]
    )
