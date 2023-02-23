from aiogram import types

from handlers.users.menu import menu
from loader import dp

from filters import IsPrivate


@dp.message_handler(IsPrivate(), text="/start")
async def command_start(message: types.Message):
    await message.answer(
        "Приветствуем вас в нашем проекте! Мы занимаемся выкупом и доставкой вещей из Китая, в основном обуви, с площадки Poison.\n"
        "Почему выбирают нас? 🤔\n"
        "Мы поможем вам купить любимые вещи по низким ценам\n"
        "Мы доставим ваш заказ быстро и безопасно 🚀\n"
        "Мы берем на себя все таможенные пошлины 💰\n"
        "Мы гарантируем качество товара 🛡️\n"
        "Для оформления заказа свяжитесь с нами в телеграм: @poison_sell_manager. Мы всегда готовы помочь вам с выбором товара и ответить на любые вопросы. 🤗\n"
        "Выбирайте наш сервис и наслаждайтесь покупками! 🛍️")
    await menu(message)
