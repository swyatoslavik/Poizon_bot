from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from google_sheets import PROMOCODES, USERS
from handlers.users.menu import menu
from keyboards.default import kb_return
from loader import dp
from states.promocode import Promocode


@dp.message_handler(Command("promocode"))
async def command_promocode(message: types.Message):
    await message.answer("Введите промокод:", reply_markup=kb_return)
    await Promocode.promo.set()


@dp.message_handler(state=Promocode.promo)
async def promocode(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    if not PROMOCODES.find(answer):
        await message.answer(f"Промокод {answer} не найден!\nПовторите попытку ввода:", reply_markup=kb_return)
        await Promocode.promo.set()
        return

    promocode_info = PROMOCODES.row_values(PROMOCODES.find(answer).row)
    user_id = message.from_user.id
    if int(promocode_info[2]) == 0:
        await message.answer(f"Промокод {answer} недействителен")
    elif str(user_id) in promocode_info[3]:
        await message.answer(f"Вы уже использовали промокод {answer}")
    else:
        promocode_value = promocode_info[1]
        await message.answer(
            f"Промокод на сумму {promocode_value} успешно активирован и будет автоматически применён при следующем заказе!")
        balance = USERS.cell(USERS.find(str(user_id)).row, 4).value
        USERS.update_cell(USERS.find(str(user_id)).row, 4, str(int(balance) + int(promocode_value)))
        cell = PROMOCODES.find(answer)
        users = PROMOCODES.cell(cell.row, 3).value
        PROMOCODES.update_cell(cell.row, 3, str(int(users) - 1))
        list_users = str(PROMOCODES.cell(cell.row, 4).value)
        PROMOCODES.update_cell(cell.row, 4, list_users + f" {str(user_id)}")
    await state.finish()
    await menu(message)
