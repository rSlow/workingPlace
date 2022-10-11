import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from io import BytesIO
import zipfile
from .stage_gather import stage_gather

PHOTOS = "photos"


async def init_photos_proxy(state: FSMContext):
    async with state.proxy() as data:
        data[PHOTOS] = []


async def add_photo_file_id(state: FSMContext, file_id: str):
    async with state.proxy() as data:
        if data.get(PHOTOS) is None:
            data[PHOTOS] = []
        data[PHOTOS].append(file_id)


async def get_file_id_list(state: FSMContext) -> list[str]:
    async with state.proxy() as data:
        return data[PHOTOS]


async def download_photo(file_id: str, bot):
    file = await bot.get_file(file_id)
    photo_io: BytesIO = await bot.download_file(file_path=file.file_path)
    return photo_io


async def get_zip(file_id_list: list[str], bot):
    tasks = []
    for i, file_id in enumerate(file_id_list, 1):
        tasks.append(download_photo(file_id=file_id, bot=bot))
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
