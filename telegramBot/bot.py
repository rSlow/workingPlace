import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class CustomBot(Bot):
    admins = list(map(int, os.getenv("ADMINS").split(",")))


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

token = os.getenv("BOT_TOKEN")

bot = CustomBot(token=token, parse_mode="HTML")
dispatcher = Dispatcher(bot=bot, storage=storage)
