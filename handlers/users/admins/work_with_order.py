from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins_id

from google_sheets import ORDERS

from handlers.users.admins.admins_menu import menu

from keyboards.default import kb_statuses, admins_menu, kb_return, kb_select_change
from loader import dp
from states.admins import ChangeOrderStatus, ChangeOrder, ChangeOrderName, ChangeOrderCost, ChangeOrderLink, \
    ChangeOrderPhoto

from datetime import datetime


@dp.message_handler(state=ChangeOrder.order_number, user_id=admins_id)
async def get_order_info(message: types.Message, state: FSMContext):
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
    await state.update_data(order_number=answer)
    user = await dp.bot.get_chat(order_info[1])
    text = ""
    text += (f"#{order_info[0]}\n"
             f"\t\t\t\t username:\t\t@{user.username}\n"
             f"\t\t\t\t Название:\t\t{order_info[2]}\n"
             f"\t\t\t\t Статус:\t\t{order_info[4]}\n"
             f"\t\t\t\t Стоимость:\t\t{order_info[5]} руб\n"
             f"\t\t\t\t Ссылка:\t\t{order_info[3]}")
    await dp.bot.send_photo(message.chat.id, photo=order_info[6], caption=text, reply_markup=kb_statuses)
    await message.answer("Выберите тип изменения:", reply_markup=kb_select_change)
    await ChangeOrder.type_of_change.set()


@dp.message_handler(state=ChangeOrder.type_of_change, user_id=admins_id)
async def select_type_of_change(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return
    elif answer == "🔄Изменить статус":
        await message.answer("Выберите новый статус для заказа:", reply_markup=kb_statuses)
        await ChangeOrderStatus.change_status.set()
    elif answer == "💭Изменить название":
        await message.answer("Введите новое название заказа:", reply_markup=kb_return)
        await ChangeOrderName.new_order_name.set()
    elif answer == "💰Изменить стоимость":
        await message.answer("Введите новую стоимость заказа:", reply_markup=kb_return)
        await ChangeOrderCost.new_order_cost.set()
    elif answer == "🔗Изменить ссылку":
        await message.answer("Введите новую ссылку заказа:", reply_markup=kb_return)
        await ChangeOrderLink.new_order_link.set()
    elif answer == "📷Изменить фотографию":
        await message.answer("Отправьте новую фотографию заказа:", reply_markup=kb_return)
        await ChangeOrderPhoto.new_order_photo.set()


@dp.message_handler(state=ChangeOrderName.new_order_name, user_id=admins_id)
async def change_order_name(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    data = await state.get_data()
    order_number = data.get("order_number")
    row_number = ORDERS.findall(order_number, in_column=1)[0].row
    ORDERS.update_cell(row_number, 3, answer)
    await state.finish()
    await change_order_final(message, order_number)


@dp.message_handler(state=ChangeOrderStatus.change_status, user_id=admins_id)
async def change_order_status(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    data = await state.get_data()
    order_number = data.get("order_number")
    await state.update_data(change_status=answer)
    ORDERS.update_cell(ORDERS.find(order_number).row, 5, answer)

    now = datetime.now()
    formatted_date_time = now.strftime("%d-%m-%Y %H:%M")
    old_history_of_statuses = ORDERS.cell(ORDERS.find(str(order_number)).row, 8).value
    history_of_statuses = str(old_history_of_statuses) + "\n" + str(answer) + "  " + str(formatted_date_time)
    ORDERS.update_cell(ORDERS.find(order_number).row, 8, history_of_statuses)

    await dp.bot.send_message(int(ORDERS.cell(ORDERS.find(order_number).row, 2).value),
                              f"Вашему заказу #{order_number} присвоен новый статус - {answer}")
    price = ORDERS.cell(ORDERS.find(str(order_number)).row, 6).value
    if answer == "ожидает оплаты":
        kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton("Подтвердить оплату✅", callback_data=f"confirm_order_payment_{order_number}")
        kb.add(button)
        await dp.bot.send_message(int(ORDERS.cell(ORDERS.find(order_number).row, 2).value),
                                  "Доставка по России 🇷🇺 оплачивается отдельно. Отправляем🚛 через Boxberry, DPD, Почту России, СДЭК или Авито Доставку 📦. Самовывоз - бесплатно😊\n"
                                  "Мы выкупаем товар в течение 12 часов⏳ после оплаты. Товар будет у нас примерно через 25 дней. Вы сможете отслеживать👀 посылку через нашего бота.\n"
                                  f"Готовы оформить заказ? Тогда переведите <b>{price}</b> рублей на любую, удобную для вас карту из списка (для копирования номера карты просто нажмите на него):\n"
                                  "     Тинькофф - <code>2200 7004 4459 5085</code> Святослав Ильич О\n"
                                  "     Сбер - <code>2202 2061 1929 4283</code> Святослав Ильич О\n"
                                  "     Альфа-Банк - <code>5559 4941 7261 0312</code> Святослав Ильич О\n"
                                  "Пожалуйста, проверяйте получателя при переводе💳. С момента получения сообщения, на оплату дается 30 минут⏰, т.к. цена за товар может измениться.\n"
                                  "Оплатите и нажмите кнопку Подтвердить оплату✅", reply_markup=kb)

    await state.finish()
    await change_order_final(message, order_number)


@dp.message_handler(state=ChangeOrderCost.new_order_cost, user_id=admins_id)
async def change_order_cost(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    data = await state.get_data()
    order_number = data.get("order_number")
    row_number = ORDERS.findall(order_number, in_column=1)[0].row
    ORDERS.update_cell(row_number, 6, answer)
    await state.finish()
    await change_order_final(message, order_number)


@dp.message_handler(state=ChangeOrderLink.new_order_link, user_id=admins_id)
async def change_order_link(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    data = await state.get_data()
    order_number = data.get("order_number")
    row_number = ORDERS.findall(order_number, in_column=1)[0].row
    ORDERS.update_cell(row_number, 4, answer)
    await state.finish()
    await change_order_final(message, order_number)


@dp.message_handler(state=ChangeOrderPhoto.new_order_photo, user_id=admins_id)
async def change_order_photo(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    data = await state.get_data()
    order_number = data.get("order_number")
    row_number = ORDERS.findall(order_number, in_column=1)[0].row
    answer = message.photo[-1].file_id
    ORDERS.update_cell(row_number, 7, answer)
    await state.finish()
    await change_order_final(message, order_number)


async def change_order_final(message: types.Message, order_number):
    await message.answer("Данные успешно обновлены.", reply_markup=admins_menu)
    order_info = ORDERS.row_values(ORDERS.find(order_number).row)
    user = await dp.bot.get_chat(order_info[1])

    text = ""
    text += (f"#{order_info[0]}\n"
             f"\t\t\t\t username:\t\t@{user.username}\n"
             f"\t\t\t\t Название:\t\t{order_info[2]}\n"
             f"\t\t\t\t Статус:\t\t{order_info[4]}\n"
             f"\t\t\t\t Стоимость:\t\t{order_info[5]} руб\n"
             f"\t\t\t\t Ссылка:\t\t{order_info[3]}")
    await dp.bot.send_photo(message.chat.id, photo=order_info[6], caption=text, reply_markup=kb_statuses)
