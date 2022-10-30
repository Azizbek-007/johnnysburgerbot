from aiogram import types
from loader import dp, bot
from keyboards.inline.choice_button import ProccesOkNoBtn
from utils.db_api.db import get_order, Get_Lang
from lang.message import lang

@dp.callback_query_handler(lambda call: call.data.startswith("ZakazOK"))
async def bot_OrderOk(call: types.CallbackQuery):
    user_data = call.data.split("=")
    try:
        loc_data = await bot.copy_message(-1001529956244, call.message.chat.id,call.message.reply_to_message.message_id )
        await call.message.copy_to(-1001529956244, reply_markup=ProccesOkNoBtn(user_data[1], user_data[2]), reply_to_message_id=loc_data.message_id)
        await bot.delete_message(call.message.chat.id, call.message.reply_to_message.message_id)
    except:
        await call.message.copy_to(-1001529956244, reply_markup=ProccesOkNoBtn(user_data[1], user_data[2]), reply_to_message_id=0)
    await call.message.delete()

@dp.callback_query_handler(lambda call: call.data.startswith("OrderNo") or call.data.startswith("proccessNo"))
async def bot_OrderOk(call: types.CallbackQuery):
    user_id = call.data.split("=")[1]
    user_lang = Get_Lang(call.from_user.id)
    try: 
        await bot.delete_message(call.message.chat.id, call.message.reply_to_message.message_id)
        await bot.send_message(user_id, lang.get('order_cancel').get(user_lang))
    except: 
        await bot.send_message(user_id, lang.get('order_cancel').get(user_lang))
    await call.message.delete()

@dp.callback_query_handler(lambda call: call.data.startswith("processOk"))
async def bot_OrderOk(call: types.CallbackQuery):
    try:await bot.delete_message(call.message.chat.id, call.message.reply_to_message.message_id)
    except: pass
    user_data = call.data.split("=")
    text = str(get_order(user_data[2]))
    ex = text.split('998')[1][2::].split(' ')[0]
    text = text.replace(ex, ' *** ** **')
    await bot.send_message(-1001633143672, text)
    user_lang = Get_Lang(call.from_user.id)
    await bot.send_message(user_data[1], lang.get('send_order').get(user_lang))
    await call.message.delete()
