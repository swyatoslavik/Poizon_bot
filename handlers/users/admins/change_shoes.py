from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id
from google_sheets import MAIN_DATA
from handlers.users.admins.admins_menu import menu
from loader import dp

from keyboards.default import admins_menu

from states.admins import ChangeShoes


@dp.message_handler(state=ChangeShoes.new_num, user_id=admins_id)
async def change_shoes(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    if not answer.isdigit():
        await message.answer("Введённое число должно быть целым")
        await ChangeShoes.new_num.set()
        return

    MAIN_DATA.update("B2", answer)
    await message.answer(f"Данные успешно обновлены. Текущая цена доставки обуви: {answer}")
    await state.finish()
    await menu(message)
