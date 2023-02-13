from aiogram.dispatcher.filters.state import StatesGroup, State


class DownloadVideoNote(StatesGroup):
    main = State()
    download = State()
