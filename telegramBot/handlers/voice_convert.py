from asyncio import sleep
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InputFile
from aiogram.types import ContentTypes
from FSM.start import Start
from FSM.convert_voice import ConvertVoice
from bot import dispatcher
from keyboards.start import StartKeyboard
from keyboards.voice_convert import ConvertVideoKeyboard, ConvertAgainVideoKeyboard


@dispatcher.message_handler(Text(equals=ConvertAgainVideoKeyboard.Buttons.again), state=ConvertVoice.convert)
@dispatcher.message_handler(Text(equals=StartKeyboard.Buttons.convert_voice), state=Start.main)
async def convert_voice_message_start(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data.clear()

    await ConvertVoice.start.set()
    await message.answer(
        text=f"Ожидаю голосовое сообщение...\n"
             f"Можно отправить перед голосовым текст, который возьмется за название файла.",
        reply_markup=ConvertVideoKeyboard()
    )


@dispatcher.message_handler(state=ConvertVoice.start, content_types=ContentTypes.TEXT)
async def set_voice_file_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["VOICE_NAME"] = message.text

    inf_msg = await message.answer(
        text=f"Название <i>{message.text}</i> принято.",
    )
    await sleep(2)
    await inf_msg.delete()


@dispatcher.message_handler(state=ConvertVoice.start, content_types=ContentTypes.VOICE)
async def convert_voice_message(message: Message, state: FSMContext):
    await ConvertVoice.convert.set()

    async with state.proxy() as data:
        filename = data.get("VOICE_NAME", None)
        if filename is None:
            filename = datetime.now().isoformat()

    voice_file_io = await message.bot.download_file_by_id(
        file_id=message.voice.file_id
    )
    voice_file = InputFile(
        path_or_bytesio=voice_file_io,
        filename=f"{filename}.mp3"
    )
    await message.answer_document(
        document=voice_file
    )
    await message.answer(
        text="Что делаем дальше?",
        reply_markup=ConvertAgainVideoKeyboard()
    )
