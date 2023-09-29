import logging
from data.config import ADMINS
from loader import dp


async def on_startup_notify():
    if ADMINS:
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, "Бот ишга тушди!!!")

            except Exception as err:
                logging.exception(err)
    pass
