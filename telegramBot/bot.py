import logging
import os

from aiogram import Bot, Dispatcher

from FSM.memory_storage import ModifiedMemoryStorage


class CustomBot(Bot):
    admins = list(map(int, os.getenv("ADMINS").split(",")))


logging.basicConfig(level=logging.INFO)
storage = ModifiedMemoryStorage()

token = os.getenv("BOT_TOKEN")

bot = CustomBot(token=token, parse_mode="HTML")
dispatcher = Dispatcher(bot=bot, storage=storage)
