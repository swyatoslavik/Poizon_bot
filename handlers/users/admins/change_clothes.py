from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id
from google_sheets import MAIN_DATA
from handlers.users.admins.admins_menu import menu
from keyboards.default import kb_return, admins_menu
from loader import dp

from states.admins import ChangeClothes

@dp.message_handler(state=ChangeClothes.new_num, user_id=admins_id)
async def change_clothes(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    if not answer.isdigit():
        await message.answer("Введённое число должно быть целым", reply_markup=kb_return)
        await ChangeClothes.new_num.set()
        return

    MAIN_DATA.update("C2", answer)
    await message.answer(f"Данные успешно обновлены. Текущая цена доставки одежды: {answer}", reply_markup=admins_menu)
