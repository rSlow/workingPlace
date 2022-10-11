import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, PhotoSize, InputFile
from io import BytesIO
import zipfile
from .stage_gather import stage_gather

PHOTOS = "photos"


async def init_photos_proxy(state: FSMContext):
    async with state.proxy() as proxy:
        proxy[PHOTOS] = []


async def add_photo(state: FSMContext, photo_object: PhotoSize):
    async with state.proxy() as proxy:
        proxy[PHOTOS].append(photo_object)


async def get_photos_list(state: FSMContext):
    async with state.proxy() as proxy:
        return proxy[PHOTOS]


async def get_zip(photos_list: list[PhotoSize]):
    tasks = []
    for i, photo_object in enumerate(photos_list, 1):
        tasks.append(photo_object.download(destination_file=BytesIO()))
    photos_io = await stage_gather(*tasks)

    zip_io = BytesIO()
    with zipfile.ZipFile(file=zip_io, mode="w") as zip_file:
        for i, photo_io in enumerate(photos_io, 1):
            photo_io.seek(0)
            zip_file.writestr(
                zinfo_or_arcname=f"{i}.jpg",
                data=photo_io.read()
            )

    zip_io.seek(0)
    zip_file = InputFile(
        path_or_bytesio=zip_io,
        filename=f"{datetime.datetime.now().ctime()}.zip")

    return zip_file
