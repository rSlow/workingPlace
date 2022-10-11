from aiogram.dispatcher import FSMContext

PHOTOS = "photos"


async def init_photos_proxy(state: FSMContext):
    async with state.proxy() as proxy:
        proxy[PHOTOS] = []


async def add_photo(state: FSMContext, photo_file_id):
    async with state.proxy() as proxy:
        proxy[PHOTOS].append(photo_file_id)


async def get_photos_list(state: FSMContext):
    async with state.proxy() as proxy:
        return proxy[PHOTOS]


async def send_zip(photos_list: list[str]):
    pass
