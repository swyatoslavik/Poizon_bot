from aiogram import types
from aiogram.dispatcher.filters import Command

from google_sheets import USERS
from handlers.users.menu import menu
from loader import dp


@dp.message_handler(Command("start"))
async def command_start(message: types.Message):
    await message.answer(
        "Приветствуем вас в нашем проекте! Мы занимаемся выкупом и доставкой вещей из Китая, в основном обуви, с площадки Poizon.\n\n"
        "Почему выбирают нас? 🤔\n"
        "•Мы поможем вам купить любимые вещи по низким ценам\n"
        "•Мы доставим ваш заказ быстро и безопасно 🚀\n"
        "•Мы берем на себя все таможенные пошлины 💰\n"
        "•Мы гарантируем качество товара 🛡️\n\n"
        "Для оформления заказа воспользуйтесь кнопками или напишите менеджеру: @poizon_sell_manager. Мы всегда готовы помочь вам с выбором товара и ответить на любые вопросы. 🤗\n"
        "Выбирайте наш сервис и наслаждайтесь покупками! 🛍️")

    await menu(message)
    if not USERS.find(str(message.from_user.id)):
        USERS.append_row([str(message.from_user.id), message.from_user.first_name, 0, 0])

