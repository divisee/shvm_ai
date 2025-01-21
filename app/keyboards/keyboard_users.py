
# keyboards/keyboard_users.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# def main_keyboard():
#     return ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="Запрос к Мудрецу")]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )
def main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Запрос к Мудрецу", callback_data="Запрос к Мудрецу")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
def cancel_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Отменить", callback_data="Отменить")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)