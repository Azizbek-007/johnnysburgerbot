import asyncio
from aiogram import types
from loader import dp, bot, admins
from keyboards.inline.choice_button import categories_btn, cancel_btn, send_messages_btn, productss_btn, \
    products_list_btn, ProccesOkNoBtn, admin_btn
from utils.db_api import DeleteCategory, get_users
from states import Category, Send, Product
from aiogram.dispatcher import FSMContext
from utils.db_api.db import create_category, ProductRegister, GetAllProducts, DeleteProduct, get_users_count
from datetime import datetime
from .broadcast import send_message

@dp.callback_query_handler(text='#cancel', state='*', user_id=admins)
async def bot_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.delete()
    await callback_query.message.answer(f"Welcome to admin panel", reply_markup=admin_btn())

@dp.callback_query_handler(text="#AddCategory")
async def some_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Categories", reply_markup=categories_btn())

@dp.callback_query_handler(lambda call: call.data.startswith('#delete='))
async def bot_categor_delete(callback_query: types.CallbackQuery):
    category_id = callback_query.data.split('=')[1]
    DeleteCategory(category_id)
    await callback_query.answer("Kategory deleted", True)
    await callback_query.message.edit_reply_markup(categories_btn())

@dp.callback_query_handler(text='AddCategoryProcces')
async def bot_addCategory(callback_query: types.CallbackQuery, state: FSMContext):
    await Category.next()
    await callback_query.message.answer("Categorya atin kiritin':", reply_markup=cancel_btn())

@dp.message_handler(state=Category.Name, content_types=[types.ContentType.TEXT])
async def bot_upload_lobi(message: types.Message, state: FSMContext):
    create_category(message.text, '')
    await message.answer("Kategorya qosildi")
    await state.finish()
    await message.answer(f"Welcome to admin panel\nusers: {get_users_count}", reply_markup=admin_btn())

@dp.callback_query_handler(text="#AddProduct")
async def some_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Product", reply_markup=productss_btn())

@dp.callback_query_handler(lambda call: call.data.startswith("#Add="))
async def bot_add_prodeuct_procces(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(CategoryID=callback_query.data.split("=")[1])
    await Product.Name.set()
    await callback_query.message.answer("product atin kiritin:", reply_markup=cancel_btn())

@dp.message_handler(state=Product.Name)
async def bot_product_name_set(message: types.Message, state: FSMContext):
    await state.update_data(ProductName=message.text)
    await Product.next()
    await message.answer("Product senasin kiritin:", reply_markup=cancel_btn())

@dp.message_handler(state=Product.Price)
async def bot_product_price_set(message: types.Message, state: FSMContext):
    await state.update_data(ProductPrice=message.text)
    await Product.next()
    await message.answer("Producat ushun photo jiberin:", reply_markup=cancel_btn())

@dp.message_handler(state=Product.IMG, content_types=types.ContentType.ANY)
async def bot_produtc_desc_set(message: types.Message, state: FSMContext):
    if message.photo:
        image_name = message.photo[-1].file_unique_id + '.jpg'
        data = await state.get_data()
        await message.photo[-1].download('../fastfoodtexnopos/photos/' + image_name)
        ProductRegister(data['CategoryID'], data['ProductName'], data['ProductPrice'], 'https://arzu.uz/' + image_name)
        await state.finish()
        await message.answer('product qosildi')
        await message.answer(f"Welcome to admin panel\nusers: {get_users_count}", reply_markup=admin_btn())
    else:
        await message.answer('Xate maglumat\nProducat ushun photo jiberin:')
    

######################

@dp.callback_query_handler(lambda call: call.data.startswith("#products="))
async def bot_products_list(callback_query: types.CallbackQuery, state: FSMContext):
    data = GetAllProducts(callback_query.data.split("=")[1])
    if data:
        await callback_query.message.answer("Productss", reply_markup=products_list_btn(data=data))
    else: await callback_query.answer("Products tabilmadi", True)
############################

############################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

@dp.callback_query_handler(lambda call: call.data.startswith('#ProductDelete='))
async def bot_productDel(call: types.CallbackQuery):
    product_id = call.data.split("=")[1]
    DeleteProduct(product_id)
    await call.message.delete()
    await call.answer("product deleted function")

@dp.callback_query_handler(text="#SendAllMessage")
async def some_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f"Xabar turin tanlan` \nusers: {get_users_count()}", reply_markup=send_messages_btn())
    
@dp.callback_query_handler(text='#botsendmessage')
async def bot_send_message(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(type="sendmessage")
    await Send.permission.set() 
    await callback_query.message.delete()
    await callback_query.message.answer("xabar jiberin:", reply_markup=cancel_btn())

@dp.callback_query_handler(text='#botsendforward')
async def bot_send_message(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(type="botsendforward")
    await Send.permission.set()
    await callback_query.message.delete()
    await callback_query.message.answer("sizdin' xabaein'iz Forward bolip baradi xabar jiberin:", reply_markup=cancel_btn())

@dp.message_handler(content_types=[types.ContentType.ANY], state=Send.permission)
async def bot_send_all_message(message: types.Message, state: FSMContext):
    count, nosend = 0, 0   
    try:
        await state.reset_state(with_data=False)
        async with state.proxy() as data_state:
            for user_id in get_users():
                try:
                    if data_state['type'] == 'sendmessage':
                        if await message.copy_to(chat_id=user_id[0], reply_markup=message.reply_markup):
                            count += 1
                    elif data_state['type'] == 'botsendforward':
                        if await message.forward(chat_id=user_id[0]):
                            count += 1
                    if count == 1 :
                        await message.answer('sending')
                    await asyncio.sleep(.05)
                except: nosend +=1
    finally:
        await message.answer(f"{count} adamga xabar jiberildi\n{nosend} adamga jiberilmedi")
        
