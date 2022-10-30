from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from utils.db_api.db import GetAllCategory
from lang.message import lang

def web_btn(user_id, user_lang):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text=lang.get('start_btn').get(user_lang),
        web_app=WebAppInfo(url=f"https://fast-food-bot.vercel.app/{user_lang}")
        ))
    markup.add(InlineKeyboardButton(lang.get('setting').get(user_lang), callback_data='setting'))
    # markup.add(InlineKeyboardButton(lang.get('ex_lang').get(user_lang), callback_data='exlang'))
    # markup.add(InlineKeyboardButton(lang.get('edit_phone').get(user_lang), callback_data='edit_phone_number'))
    return markup

def setting_btn(user_lang):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(lang.get('ex_lang').get(user_lang), callback_data='exlang'))
    markup.add(InlineKeyboardButton(lang.get('edit_phone').get(user_lang), callback_data='edit_phone_number'))
    markup.add(InlineKeyboardButton(lang.get('back').get(user_lang), callback_data='back_main'))
    return markup

    
def admin_btn():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(
        text="category", 
        callback_data="#AddCategory"
    )
    btn2 = InlineKeyboardButton(
        text="Product",
        callback_data="#AddProduct"
    )
    btn3 = InlineKeyboardButton(
        text="Send all message",
        callback_data="#SendAllMessage"
    )

    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup

def categories_btn():
    markup = InlineKeyboardMarkup()
    for x in GetAllCategory():
        print(x)
        btn1 = InlineKeyboardButton(
            text=f"{x[1]}",
            callback_data="None"
        )
        btn2 = InlineKeyboardButton(
            text="🗑 Delete",
            callback_data=f"#delete={x[0]}"
        )
        markup.add(btn1, btn2)
    btn3 = InlineKeyboardButton(
        text="➕ Add Category",
        callback_data="AddCategoryProcces"
    )
    btn4 = InlineKeyboardButton(
        text="✖️cancel",
        callback_data="#cancel"
    )
    markup.add(btn3)
    markup.add(btn4)
    return markup

def productss_btn():
    markup = InlineKeyboardMarkup()
    for x in GetAllCategory():
        print(x)
        btn1 = InlineKeyboardButton(
            text=f"{x[1]}",
            callback_data=f"#products={x[0]}"
        )
        btn2 = InlineKeyboardButton(
            text="➕",
            callback_data=f"#Add={x[0]}"
        )
        markup.add(btn1, btn2)
    btn3 = InlineKeyboardButton(
        text="✖️cancel",
        callback_data="#cancel"
    )
    markup.add(btn3)
    return markup

def products_list_btn(data):
    markup = InlineKeyboardMarkup()
    for x in data:
        print(x)
        btn1 = InlineKeyboardButton(
            text=f"{x[1]}",
            callback_data="None"
        )
        btn2 = InlineKeyboardButton(
            text="🗑 Delete",
            callback_data=f"#ProductDelete={x[0]}"
        )
        markup.add(btn1, btn2)
    # btn3 = InlineKeyboardButton(
    #     text="✖️cancel",
    #     callback_data="#cancel"
    # )
    # markup.add(btn3)
    return markup

def cancel_btn():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="✖️cancel", callback_data="#cancel"))
    return markup

def send_messages_btn():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Send message", callback_data="#botsendmessage"))
    markup.add(InlineKeyboardButton("Send Forward", callback_data="#botsendforward"))
    markup.add(InlineKeyboardButton("✖️cancel",callback_data="#cancel"))
    return markup

def ProccesOkNoBtn(user_id, order_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Jiberildi", callback_data=f"processOk={user_id}={order_id}"),
        InlineKeyboardButton("❌ Biykarlaw", callback_data=f"proccessNo={user_id}")
        )
    return markup
    
def ZakazOkNoBtn(user_id, order_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📦 Qabillaw", callback_data=f"ZakazOK={user_id}={order_id}"),
        InlineKeyboardButton("❌ Biykarlaw", callback_data=f"proccessNo={user_id}")
        )
    return markup

def lang_btn():
    markup = InlineKeyboardMarkup()
    langs = lang.get('lang_btn')
    for d in langs:          
        markup.add(InlineKeyboardButton(str(d).split(":")[0], callback_data=str(d).split(":")[1]))
    return markup

def order_types_btn(user_lang, order_id):
    obj_lang = lang.get('kargo_btn').get(user_lang)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(obj_lang[0], callback_data=f"OrderID={order_id}"))
    markup.add(InlineKeyboardButton(obj_lang[1], callback_data=f"OrrderNo={order_id}"))
    markup.add(InlineKeyboardButton(obj_lang[2], callback_data="otmen"))
    return markup
   
