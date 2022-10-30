from aiogram.dispatcher.filters.state import StatesGroup, State


class Category(StatesGroup):
    Name = State()
    Image = State()


