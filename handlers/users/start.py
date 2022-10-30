from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, state
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate, IsRegisted
from loader import dp, bot
from utils.db_api.db import register_user, phone_update, get_order, Set_Lang, Get_Lang
from lang.message import lang
from keyboards.inline.choice_button import web_btn, ZakazOkNoBtn, ZakazOkNoBtn, lang_btn, order_types_btn, setting_btn
from keyboards.default import phone, remov, keyboard_loc
from states import Form, Location


@dp.message_handler(IsRegisted(), CommandStart(), IsPrivate(), state='*')
@dp.throttled(rate=1)
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer('🍔', reply_markup=remov)
    user_lang = Get_Lang(message.from_user.id)
    await message.answer(lang.get('start').get(user_lang), reply_markup=web_btn(message.from_user.id, user_lang))
    await state.finish()

@dp.message_handler(CommandStart(), IsPrivate(), state='*')
@dp.throttled(rate=1)
async def bot_start(message: types.Message):
    register_user(message.from_id, message.from_user.first_name, message.from_user.username)
    await Form.next()
    user_lang = Get_Lang(message.from_user.id)
    await message.answer(lang.get('send_nummber').get(user_lang), reply_markup=phone(user_lang))

@dp.message_handler(Command('lang'))
async def set_lang(msg: types.Message):
    await msg.answer(lang.get('lang'), reply_markup=lang_btn())

@dp.callback_query_handler(lambda call: call.data == 'exlang')
async def call_ex_lang(call: types.CallbackQuery):
    await call.message.edit_text(lang.get('lang'), reply_markup=lang_btn())

@dp.callback_query_handler(lambda call: call.data == 'back_main')
async def back_main(call: types.CallbackQuery):
    user_lang = Get_Lang(call.from_user.id)
    await call.message.edit_text(lang.get('start').get(user_lang), reply_markup=web_btn(call.from_user.id, user_lang))

@dp.callback_query_handler(lambda call: call.data == 'setting')
async def setting_bot(call: types.CallbackQuery):
    user_lang = Get_Lang(call.from_user.id)
    text = str(lang.get('setting').get(user_lang)).replace('⚙️', '')
    await call.message.edit_text(text, reply_markup=setting_btn(user_lang))

@dp.callback_query_handler(lambda call: call.data in ['qq', 'ru', 'uz'])
async def set_db_lang(call: types.CallbackQuery):
    Set_Lang(call.data, call.from_user.id)
    user_lang = Get_Lang(call.from_user.id)
    await call.message.edit_text(lang.get('start').get(user_lang), reply_markup=web_btn(call.from_user.id, user_lang))

@dp.callback_query_handler(lambda call: call.data == 'edit_phone_number')
async def update_user_phone_number(call: types.CallbackQuery):
    await Form.next()
    user_lang = Get_Lang(call.from_user.id)
    await call.message.answer(lang.get('send_nummber').get(user_lang), reply_markup=phone(user_lang))

@dp.message_handler(state=Form.Phone, content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def bot_phone(message: types.Message, state: FSMContext):
    user_lang = Get_Lang(message.from_user.id)
    try:
        phone_number = message.contact.phone_number
    except:  phone_number = message.text
    if phone_number in ' ': phone_number.replace(' ')

    if phone_number[:3] == '998' or phone_number[:4] == '+998':
        if phone_number[0] != '+': phone_number = '+' + phone_number 
        phone_update(message.from_user.id, phone_number)
        await message.reply("✅", reply_markup=remov)
        await message.answer(lang.get('start').get(user_lang), reply_markup=web_btn(message.from_user.id, user_lang))
        await state.finish()
    else: await message.answer(lang.get('erro_nummber').get(user_lang), reply_markup=phone(user_lang))


@dp.callback_query_handler(lambda call: call.data == 'otmen')
async def bot_OrderNo(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_lang = Get_Lang(call.from_user.id)
    await call.message.answer(lang.get('order_cancel').get(user_lang))
    await call.message.answer(lang.get('start').get(user_lang), reply_markup=web_btn(call.from_user.id, user_lang))
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith("OrrderNo"))
async def bot_OrderNo(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    order_id = str(call.data).split('=')[1]
    text = get_order(order_id)
    user_lang = Get_Lang(call.from_user.id)
    await call.message.answer(lang.get('order_ok').get(user_lang))
    await bot.send_message(-1001870744170, f"#{order_id}\n\n{text}", reply_markup=ZakazOkNoBtn(call.from_user.id, order_id))
    user_lang = Get_Lang(call.from_user.id)
    await call.message.answer(lang.get('start').get(user_lang), reply_markup=web_btn(call.from_user.id, user_lang))
    await state.finish()
    
@dp.callback_query_handler(lambda call: call.data.startswith("OrderID"))
async def bot_OrderOk(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    order_id = call.data.split("=")[1]
    text = str(get_order(order_id)).split('summa:')[1].split('\n')[0]
    _text = ""
    if int(text) >= 50000:
        _text = _text + "\n\nbiypul jetkizip beriw"
    else: _text = _text + "\n\ntolemli jetkizip beriw"
    user_lang = Get_Lang(call.from_user.id)
    await state.update_data(order_id=order_id)
    await state.set_state(Location.Proms)
    await call.message.answer(lang.get('location').get(user_lang) + _text, reply_markup=keyboard_loc(user_lang))


@dp.message_handler(state=Location.Proms, content_types=[types.ContentType.ANY])
async def bot_get_location(msg: types.Message, state: FSMContext):
    user_lang = Get_Lang(msg.from_user.id)
    user_data = await state.get_data()
    if msg.location:
        text = get_order(user_data['order_id'])
        loc = await msg.copy_to(-1001870744170)
        await bot.send_message(chat_id=-1001870744170, text=f"#{user_data['order_id']}\n\n{text}", reply_markup=ZakazOkNoBtn(user_id=msg.from_user.id, order_id=user_data['order_id']), reply_to_message_id=loc.message_id)
        await  msg.answer(lang.get('order_ok').get(user_lang), reply_markup=remov)
        await msg.answer(lang.get('start').get(user_lang), reply_markup=web_btn(msg.from_user.id, user_lang))
        await state.finish()
    elif msg.text == lang.get('back').get(user_lang):
        await msg.answer('🍔', reply_markup=remov)
        await msg.answer(lang.get('kargo').get(user_lang), reply_markup=order_types_btn(user_lang, user_data['order_id']))
        await state.finish()
    else: await msg.answer(lang.get('error_msg').get(user_lang))
