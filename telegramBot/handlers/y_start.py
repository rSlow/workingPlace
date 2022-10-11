from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from FSM.start import Start
from bot import dispatcher
from keyboards.start import StartKeyboard


@dispatcher.message_handler(commands=["start", "help"], state="*")
async def start(message: types.Message):
    await Start.main.set()

    await message.answer(
        text="Добро пожаловать. Выберите действие:",
        reply_markup=StartKeyboard()
    )


@dispatcher.message_handler(
    Text(equals=StartKeyboard.on_main_button),
    state="*"
)
async def on_main(message: types.Message):
    await Start.main.set()

    await message.answer(
        text="Возвращаем в главное меню...",
        reply_markup=StartKeyboard()
    )
