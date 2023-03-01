import os

from aiogram import types
from aiogram.types import ParseMode

from data.config import admins_id

from google_sheets import MAIN_DATA, ORDERS
from handlers.users.admins.admins_menu import menu
from handlers.users.menu import menu as user_menu

from keyboards.default import kb_return
from loader import dp
from states.admins import ChangeCourse, ChangeShoes, ChangeClothes, ChangeCommission, ChangeOrder, AddPromocode


@dp.message_handler(text="💴Изменить курс юаня", user_id=admins_id)
async def command_calculate_cource(message: types.Message):
    cource = MAIN_DATA.acell("A2").value
    await message.answer(f"Текущий курс юаня: {cource}\n"
                         "Введите новое число:", reply_markup=kb_return)
    await ChangeCourse.new_num.set()


@dp.message_handler(text="👟Изменить обувь", user_id=admins_id)
async def command_calculate_shoes(message: types.Message):
    cource = MAIN_DATA.acell("B2").value
    await message.answer(f"Текущая цена доставки обуви: {cource}\n"
                         "Введите новое число:", reply_markup=kb_return)
    await ChangeShoes.new_num.set()


@dp.message_handler(text="👔Изменить одежду/аксы", user_id=admins_id)
async def command_calculate_clothes(message: types.Message):
    cource = MAIN_DATA.acell("C2").value
    await message.answer(f"Текущая цена доставки одежды: {cource}\n"
                         "Введите новое число:", reply_markup=kb_return)
    await ChangeClothes.new_num.set()


@dp.message_handler(text="💰Изменить комиссию", user_id=admins_id)
async def command_calculate_clothes(message: types.Message):
    cource = MAIN_DATA.acell("D2").value
    await message.answer(f"Текущая комиссия сервиса: {cource}\n"
                         "Введите новое число:", reply_markup=kb_return)
    await ChangeCommission.new_num.set()


@dp.message_handler(text="📋Список заказов", user_id=admins_id)
async def command_calculate_clothes(message: types.Message):
    list_of_dicts = ORDERS.get_all_records()
    list_of_orders = []
    for slovar in list_of_dicts:
        user = await dp.bot.get_chat(slovar["user_id"])
        list_of_orders.append([user.username,
                               slovar["order_number"],
                               slovar["order_name"],
                               slovar["status"],
                               slovar["price"],
                               slovar["link"]])
    text = ""
    for order in list_of_orders:
        text += (f"#{order[1]}\n"
                 f"\t\t\t\t username:\t\t@{order[0]}\n"
                 f"\t\t\t\t Название:\t\t{order[2]}\n"
                 f"\t\t\t\t Статус:\t\t{order[3]}\n"
                 f"\t\t\t\t Стоимость:\t\t{order[4]}₽\n"
                 f"\t\t\t\t Ссылка: \t\t{order[5]}\n\n")
    text = text.encode('utf-8')
    with open('./media/list_of_orders.txt', 'wb') as file:
        file.write(text)
    with open('./media/list_of_orders.txt', 'rb') as file:
        await dp.bot.send_document(chat_id=message.from_user.id, document=file)
        await menu(message)


@dp.message_handler(text="🔄Обработать заказ", user_id=admins_id)
async def work_with_orders(message: types.Message):
    await message.answer("Введите номер заказа", reply_markup=kb_return)
    await ChangeOrder.order_number.set()

@dp.message_handler(text="🎟Добавить промокод", user_id=admins_id)
async def work_with_orders(message: types.Message):
    await message.answer("Введите новый промокод, значение и количество активаций через пробел(по умолчанию - 1)", reply_markup=kb_return)
    await AddPromocode.promocode.set()

@dp.message_handler(text="🏠Главное меню", user_id=admins_id)
async def work_with_orders(message: types.Message):
    await user_menu(message)
