from aiogram import types

from bot import dispatcher
from aiogram.types import ContentTypes

@dispatcher.message_handler(state="*", content_types=ContentTypes.ANY)
async def delete(message: types.Message):
    await message.delete()
