import logging


async def on_startup(_):
    try:
        import handlers
    except ImportError as ex:
        logging.warn(msg=ex)


async def on_shutdown(_):
    pass
