from aiogram.dispatcher.filters.state import StatesGroup, State


class ImagesZip(StatesGroup):
    start = State()
    waiting = State()
    finish = State()
