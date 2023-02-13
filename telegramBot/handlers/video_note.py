from datetime import datetime

from aiogram.dispatcher.filters import Text
from aiogram.types import ContentTypes, Message
from aiogram.types import InputFile

from FSM.start import Start
from FSM.video_note import DownloadVideoNote
from bot import dispatcher
from handlers.y_start import on_main
from keyboards.start import StartKeyboard
from keyboards.video_note import DownloadVideoKeyboard


@dispatcher.message_handler(Text(equals=StartKeyboard.Buttons.download_video_note), state=Start.main)
async def download_video_note_start(message: Message):
    await DownloadVideoNote.main.set()
    await message.answer(
        text="Ожидаю кружочек...",
        reply_markup=DownloadVideoKeyboard()
    )


@dispatcher.message_handler(content_types=ContentTypes.VIDEO_NOTE, state=DownloadVideoNote.main)
async def download_video_note(message: Message):
    await DownloadVideoNote.download.set()
    receive_message = await message.answer("Видеосообщение принято, обработка...")
    video_note_file_io = await message.bot.download_file_by_id(
        file_id=message.video_note.file_id
    )
    video_note = InputFile(
        path_or_bytesio=video_note_file_io,
        filename=f"{datetime.now().isoformat()}.mp4"
    )
    await receive_message.delete()
    send_message = await message.answer("Видео отправляется...")
    await message.answer_document(
        document=video_note
    )
    await send_message.delete()
    await on_main(message=message)
