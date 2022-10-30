from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from lang.message import lang

def phone(user_lang):
    return ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text=lang.get("send_nummber_btn").get(user_lang), request_contact=True)
    ],
    ],
    resize_keyboard=True
    )

remov = ReplyKeyboardRemove()