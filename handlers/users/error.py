from aiogram import types

from handlers.users.menu import menu
from loader import dp


@dp.message_handler()
async def command_error(message: types.Message):
    await message.answer("🌧 Неизвестная команда")
    await menu(message)
