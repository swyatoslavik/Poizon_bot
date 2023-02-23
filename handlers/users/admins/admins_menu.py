from aiogram.dispatcher.filters import Command
from aiogram import types

from data.config import admins_id
from loader import dp

from keyboards.default import admins_menu


@dp.message_handler(Command("admin"), user_id=admins_id)
async def menu(message: types.Message):
    await message.answer("Главное меню администратора:", reply_markup=admins_menu)
