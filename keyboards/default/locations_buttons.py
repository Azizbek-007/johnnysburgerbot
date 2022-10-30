from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.message import lang

def keyboard_loc(user_lang):
    return ReplyKeyboardMarkup(
        keyboard=
        [
            [
                KeyboardButton(text=lang.get('location_btn').get(user_lang), request_location=True),
                KeyboardButton(text=lang.get('back').get(user_lang))
            ]
        ],
        resize_keyboard=True
    )