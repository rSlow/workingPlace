from aiogram import executor

from bot import dispatcher
from utils import startup_shutdown

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher,
                           skip_updates=True,
                           on_startup=startup_shutdown.on_startup,
                           on_shutdown=startup_shutdown.on_shutdown)
