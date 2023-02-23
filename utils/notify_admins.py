import logging

from aiogram import Dispatcher

from data.config import admins_id


async def on_startup_notify(dp: Dispatcher):
    for admin_id in admins_id:
        try:
            text = "Бот запущен"
            await dp.bot.send_message(admin_id, text)
        except Exception as err:
            logging.exception(err)
