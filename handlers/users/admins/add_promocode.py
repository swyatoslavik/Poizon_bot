from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id
from google_sheets import PROMOCODES

from handlers.users.admins.admins_menu import menu
from loader import dp

from states.admins import AddPromocode


@dp.message_handler(state=AddPromocode.promocode, user_id=admins_id)
async def add_promo(message: types.Message, state: FSMContext):
    answer = message.text
    print(answer)
    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    try:
        promo, value, num = answer.split()
    except Exception:
        try:
            promo, value = answer.split()
            num = 1
        except Exception:
            promo = answer
            value = "100"
            num = 1
    for _ in range(int(num)):
        PROMOCODES.append_row([promo, value, "June"])
    await message.answer(f"Промокод {promo} на сумму {value} в количестве {num} успешно добавлен")
    await menu(message)
    await state.finish()
