import logging

from ORM.base import init_database
from bot import storage


async def on_startup(_):
    try:
        import handlers
    except ImportError as ex:
        logging.warn(msg=ex)

    await init_database()
    await storage.set_all_states()


async def on_shutdown(_):
    pass
