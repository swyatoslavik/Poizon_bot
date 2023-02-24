from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id
from google_sheets import MAIN_DATA
from handlers.users.admins.admins_menu import menu
from keyboards.default import admins_menu, kb_return
from loader import dp

from states.admins import ChangeCourse


@dp.message_handler(state=ChangeCourse.new_num, user_id=admins_id)
async def change_cource(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    if not answer.replace('.', '', 1).isdigit():
        await message.answer("Введённое число должно быть целым или с точкой", reply_markup=kb_return)
        await ChangeCourse.new_num.set()
        return

    MAIN_DATA.update("A2", answer)
    await message.answer(f"Данные успешно обновлены. Текущий курс: {answer}")
    await state.finish()
    await menu(message)
