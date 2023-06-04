from aiogram.dispatcher.filters.state import StatesGroup, State


class ConvertVoice(StatesGroup):
    start = State()
    convert = State()
