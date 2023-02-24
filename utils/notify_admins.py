import logging

from aiogram import Dispatcher




async def on_startup_notify(dp: Dispatcher):
        try:
            text = "Бот запущен"
            await dp.bot.send_message(473151013, text)
        except Exception as err:
            logging.exception(err)
