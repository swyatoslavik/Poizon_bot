from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id
from google_sheets import MAIN_DATA

from handlers.users.admins.admins_menu import menu
from keyboards.default import admins_menu, kb_return
from loader import dp

from states.admins import ChangeCommission

@dp.message_handler(state=ChangeCommission.new_num, user_id=admins_id)
async def change_clothes(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    if not answer.isdigit():
        await message.answer("Введённое число должно быть целым", kb_return)
        await ChangeCommission.new_num.set()
        return

    MAIN_DATA.update("D2", answer)
    await message.answer(f"Данные успешно обновлены. Текущая комиссия сервиса: {answer}", reply_markup=admins_menu)
