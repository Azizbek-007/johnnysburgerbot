from aiogram import types
from loader import dp, admins
from keyboards.inline.choice_button import admin_btn
from utils.db_api.db import get_users_count

@dp.message_handler(commands=['admin'], user_id=admins)
async def bot_admin(message: types.Message):
    await message.answer(f"Welcome to admin panel", reply_markup=admin_btn())
    