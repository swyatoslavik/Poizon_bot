import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram import types

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the bot and dispatcher
bot = Bot(token="6267875289:AAEYLSp4hC8UcLm_d2qtm94g1zwPC1tEU7M")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Define the welcome message
async def send_welcome(message: types.Message):
    await message.reply("Всем привет ✋👋 , заказываем вещи с пойзона по низкой наценке.Нужны кроссовки, майки и "
                        "тд.- пиши нам, всё расчитаем, что бы убедится что это не скам можете посмотреть отзывы на "
                        "авито.Сейчас курс 11,5 , цена за нашу услугу указана в объявление. Вещи идут в течении 3-4 "
                        "недель.")


# Define the main menu keyboard
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
profile_button = types.KeyboardButton("Профиль")
help_button = types.KeyboardButton("Помощь")
my_orders_button = types.KeyboardButton("Мои заказы")
create_order_button = types.KeyboardButton("Создать заказ")
main_menu_keyboard.add(profile_button, help_button, my_orders_button, create_order_button)


# Define the state machine for creating an order
class CreateOrderStates(StatesGroup):
    get_order_name = State()
    get_order_description = State()


# Define the handler for the /start command
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await send_welcome(message)
    await message.reply("Воспользуйся кнопками, чтобы отследить или создать свой заказ."
                        "Используй кнопку 'помощь', чтобы получить ответ на свой вопрос",
                        reply_markup=main_menu_keyboard)


# Define the handler for the "Profile" button
@dp.message_handler(Text(equals="Профиль"))
async def profile(message: types.Message):
    user = message.from_user
    username = user.username
    user_id = user.id
    profile_text = ("➖➖➖➖➖➖➖➖➖➖➖\n"
                    "ℹ️ Информация о вас:\n"
                    f"🔑 Логин: @{username}\n"
                    f"💳 ID: {user_id}\n"
                    "💵 Покупок на сумму: 0 руб\n"
                    "🏦 Баланс: 0 руб.\n"
                    "➖➖➖➖➖➖➖➖➖➖➖")
    await message.answer(profile_text)


# Define the handler for the "Help" button
@dp.message_handler(Text(equals="Помощь"))
async def help(message: types.Message):
    await message.reply("Чтобы оформить заказ, необходимо выполнить несколько простых действий: "
                        "заходите на poizon , выбираете товар , скидываете нам его и говорите расцветку и размер, "
                        "дальше мы считаем сколько это выходит, и от этой суммы вы оплачиваете в начале 30% , "
                        "остальное после прихода к нам вашего товара")
    await  message.reply("Если хотите задать вопрос, можете обратится к нашему менеджеру: @sickeryo")


# Define the handler for the "My Orders" button
@dp.message_handler(Text(equals="Мои заказы"))
async def my_orders(message: types.Message):
    await message.reply("Ваши заказы:")


# Define the handler for the "Create an Order" button
@dp.message_handler(Text(equals="Создать заказ"))
async def create_order(message: types.Message):
    await message.reply("Как назовём заказ? Его имя будете знать только вы")
    await CreateOrderStates.get_order_name.set()


# Define the handler for the order name
@dp.message_handler(state=CreateOrderStates.get_order_name)
async def process_order_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['order_name'] = message.text

    await message.reply("Введите ссылку на товар с Пойзона. Пример: иди нахуй")
    await CreateOrderStates.get_order_description.set()


# Define the handler for the order description
@dp.message_handler(state=CreateOrderStates.get_order_description)
async def process_order_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['order_description'] = message.text

        # Do something with the order data, e.g. store it in a database
        order_name = data['order_name']
        order_description = data['order_description']
        await message.reply(f"Заказ создан: {order_name} - {order_description}")

        # Reset the state machine
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
