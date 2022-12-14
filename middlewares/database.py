from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api.user import User


class GetDBUser(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        data["user"] = User(id=message.from_user.id, name=message.from_user.full_name)