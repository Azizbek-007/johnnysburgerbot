import asyncio
import logging
from aiogram.utils import exceptions
from loader import bot

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

async def send_message(chat_id: int, from_chat_id: int, message_id: int, reply_markup, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.copy_message(chat_id, chat_id, message_id, reply_markup)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{chat_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{chat_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(chat_id, chat_id, message_id, reply_markup)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{chat_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{chat_id}]: failed")
    else:
        log.info(f"Target [ID:{chat_id}]: success")
        return True
    return False

