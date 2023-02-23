from aiogram import types

from loader import dp

@dp.message_handler()
async def command_error(message: types.Message):
    await message.answer("🌧 Неизвестная команда")