from aiogram.dispatcher.filters.state import StatesGroup, State

class Product(StatesGroup):
    Name = State()
    Price = State()
    IMG = State()