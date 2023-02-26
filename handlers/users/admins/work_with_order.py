from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id

from google_sheets import ORDERS

from handlers.users.admins.admins_menu import menu

from keyboards.default import kb_statuses, admins_menu, kb_return
from loader import dp
from states.admins import ChangeOrderStatus
from utils.send_photo import send_image

from datetime import datetime

@dp.message_handler(state=ChangeOrderStatus.select_order, user_id=admins_id)
async def change_clothes(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return
    if not ORDERS.find(answer):
        await message.answer(f"Заказ {answer} не найден!", reply_markup=kb_return)
        await ChangeOrderStatus.select_order.set()
        return
    order_info = ORDERS.row_values(ORDERS.find(answer).row)
    await state.update_data(select_order=answer)
    user = await dp.bot.get_chat(order_info[1])
    text = ""
    text += (f"#{order_info[0]}\n"
             f"\t\t\t\t username:\t\t@{user.username}\n"
             f"\t\t\t\t Название:\t\t{order_info[2]}\n"
             f"\t\t\t\t Статус:\t\t{order_info[4]}\n"
             f"\t\t\t\t Стоимость:\t\t{order_info[5]} руб\n"
             f"\t\t\t\t Ссылка:\t\t{order_info[3]}")
    photo = await send_image(chat_id=message.chat.id, image_url=order_info[6])
    await dp.bot.send_photo(message.chat.id, photo=photo, caption=text, reply_markup=kb_statuses)
    await ChangeOrderStatus.change_status.set()


@dp.message_handler(state=ChangeOrderStatus.change_status, user_id=admins_id)
async def change_clothes(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    data = await state.get_data()
    await state.update_data(change_status=answer)
    ORDERS.update_cell(ORDERS.find(data.get("select_order")).row, 5, answer)

    now = datetime.now()
    formatted_date_time = now.strftime("%d-%m-%Y %H:%M")
    old_history_of_statuses = ORDERS.cell(ORDERS.find(str(data.get("select_order"))).row, 8).value
    history_of_statuses = str(old_history_of_statuses) + "\n" + str(answer) + "  " + str(formatted_date_time)
    ORDERS.update_cell(ORDERS.find(data.get("select_order")).row, 8, history_of_statuses)

    await message.answer("Данные успешно обновлены.", reply_markup=admins_menu)
    order_info = ORDERS.row_values(ORDERS.find(data.get("select_order")).row)
    user = await dp.bot.get_chat(order_info[1])
    text = ""
    print(order_info)
    text += (f"#{order_info[0]}\n"
             f"\t\t\t\t username:\t\t@{user.username}\n"
             f"\t\t\t\t Название:\t\t{order_info[2]}\n"
             f"\t\t\t\t Статус:\t\t{order_info[4]}\n"
             f"\t\t\t\t Стоимость:\t\t{order_info[5]} руб\n"
             f"\t\t\t\t Ссылка:\t\t{order_info[3]}")
    await message.answer(text)

    await dp.bot.send_message(int(ORDERS.cell(ORDERS.find(data.get("select_order")).row, 2).value),
                              f"Ваш заказ #{data.get('select_order')} получил новый статус: {answer}")

    await state.finish()
    await menu(message)
