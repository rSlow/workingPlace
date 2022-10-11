from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from FSM.start import Start
from FSM.images_zip import ImagesZip
from bot import dispatcher
from keyboards.start import StartKeyboard
from keyboards.pack import PackKeyboard, PackAgainKeyboard
from keyboards.pack import PackKeyboardButtons, PackAgainKeyboardButtons
from utils import photos


@dispatcher.message_handler(
    Text(equals=StartKeyboard.Buttons.pack),
    state=Start.main
)
async def wait_photos(message: types.Message, state: FSMContext):
    await ImagesZip.start.set()

    await photos.init_photos_proxy(state)

    await message.answer(
        text="Жду фотографий. Как отправлены все - нажать 'Запаковать!'",
        reply_markup=PackKeyboard()
    )


@dispatcher.message_handler(
    content_types=ContentType.PHOTO,
    state=[ImagesZip.start, ImagesZip.waiting]
)
async def append_photo(message: types.Message, state: FSMContext):
    await ImagesZip.waiting.set()

    file_id = message.photo[-1].file_id
    await photos.add_photo_file_id(state, file_id)
    await message.delete()


@dispatcher.message_handler(
    Text(equals=PackKeyboardButtons.accept),
    state=ImagesZip.waiting
)
async def return_zip(message: types.Message, state: FSMContext):
    file_id_list = await photos.get_file_id_list(state)

    if not file_id_list:
        await message.answer(
            text="Не было отправлено ни одной фотографии, пробуем еще раз!"
        )
        await wait_photos(message=message, state=state)

    else:
        temp_message = await message.answer(
            text=f"Запаковывается {len(file_id_list)} фотографий..."
        )

        await ImagesZip.finish.set()
        zip_file = await photos.get_zip(file_id_list, bot=message.bot)

        await temp_message.delete()

        temp_message = await message.answer(
            text="Архив отправляется..."
        )
        await message.answer_document(
            document=zip_file,
            reply_markup=PackAgainKeyboard()
        )
        await temp_message.delete()


@dispatcher.message_handler(
    Text(equals=PackAgainKeyboardButtons.again),
    state=ImagesZip.finish
)
async def zip_again(message: types.Message, state: FSMContext):
    await wait_photos(message=message, state=state)
