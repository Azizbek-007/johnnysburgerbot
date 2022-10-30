from aiogram.dispatcher.filters.state import StatesGroup, State

class Send(StatesGroup):
    permission = State()