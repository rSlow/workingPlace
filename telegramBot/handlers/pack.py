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

    photo_object: types.PhotoSize = message.photo[-1]
    await photos.add_photo(state, photo_object)

    await message.delete()


@dispatcher.message_handler(
    Text(equals=PackKeyboardButtons.accept),
    state=ImagesZip.waiting
)
async def return_zip(message: types.Message, state: FSMContext):
    photos_list = await photos.get_photos_list(state)

    if not photos_list:
        await message.answer(
            text="Не было отправлено ни одной фотографии, пробуем еще раз!"
        )
        await wait_photos(message=message, state=state)

    else:
        temp_message = await message.answer(
            text=f"Запаковывается {len(photos_list)} фотографий..."
        )

        await ImagesZip.finish.set()
        zip_file = await photos.get_zip(photos_list)

        await temp_message.delete()
        await message.answer_document(
            document=zip_file,
            reply_markup=PackAgainKeyboard()
        )


@dispatcher.message_handler(
    Text(equals=PackAgainKeyboardButtons.again),
    state=ImagesZip.finish
)
async def zip_again(message: types.Message, state: FSMContext):
    await wait_photos(message=message, state=state)
