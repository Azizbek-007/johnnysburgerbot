from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api.db import userBy

class IsRegisted(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        try:
            if len(userBy(message.from_user.id)) != 0:
                return True
            else: return False
        except: return True