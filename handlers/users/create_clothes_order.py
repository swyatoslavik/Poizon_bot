from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from data import config
from filters import IsPrivate
from google_sheets import ORDERS, MAIN_DATA
from handlers.users.menu import menu
from keyboards.default import kb_return
from keyboards.default.yes_no import kb_yes_no

from loader import dp, bot
from states.calculate_clothes import CalculateClothes
from states.calculate_shoes import CalculateShoes


async def check_link(link):
    import re
    link_regex = r'^https:\/\/dw4\.co\/t\/[A-Z]\/[a-zA-Z0-9]+$'
    return re.match(link_regex, link)


async def create_an_order_number():
    import random
    num = random.randint(100000, 999999)
    if ORDERS.find(str(num)):
        print("Уже есть такой заказ")
        return create_an_order_number()
    return num


async def get_photo(message):
    photo = message.photo[-1]
    photo_id = photo.file_id
    photo_file = await bot.get_file(photo_id)
    photo_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{photo_file.file_path}"
    return photo_url


@dp.message_handler(IsPrivate(), state=CalculateClothes.price)
async def get_clothes_price(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    if not answer.isdigit():
        await message.answer("Введите целое число", reply_markup=kb_return)
        await CalculateClothes.price.set()
        return

    cource = MAIN_DATA.acell('A2').value
    com_clothes = MAIN_DATA.acell("C2").value
    com_service = MAIN_DATA.acell("D2").value
    price = int(float(answer) * float(cource) + float(com_clothes) + float(com_service))
    await state.update_data(price=price)

    await message.answer(f"Стоимость вещей:\n"
                         f"<b>{price} рублей</b>")
    await message.answer("Хотите создать заказ?", reply_markup=kb_yes_no)
    await CalculateClothes.status.set()


@dp.message_handler(IsPrivate(), state=CalculateClothes.status)
async def get_clothes_status(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    await state.update_data(status=answer)
    if answer == "Да ️✅" or answer.lower() == "да":
        await message.answer("Введите название заказа на русском.\n"
                             "Это может быть название вещи, её цвет и размер, например.", reply_markup=kb_return)
        await CalculateClothes.order_name.set()
    elif answer == "Нет❌️" or answer.lower() == "нет":
        await state.finish()
        await menu(message)
        return
    else:
        await message.answer("Введён некорректный ответ, пожалуйста, воспользуйтесь клавиатурой.",
                             reply_markup=kb_yes_no)
        await CalculateClothes.status.set()


@dp.message_handler(IsPrivate(), state=CalculateClothes.order_name)
async def get_clothes_order_name(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    await state.update_data(order_name=answer)
    await message.answer("Введите ссылку на товар в формате:\n"
                         "https://dw4.co/t/A/167cOUmx")
    await CalculateClothes.link.set()


@dp.message_handler(IsPrivate(), state=CalculateClothes.link)
async def get_clothes_link(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return
    if not check_link(answer):
        await message.answer("Неверный формат ссылки. Повторите попытку.")
        await CalculateClothes.link.set()
        return
    await state.update_data(link=answer)

    await message.answer("Отправьте скриншот, на котором будет видно: Товар, размер, цвет")
    await CalculateClothes.photo.set()


@dp.message_handler(IsPrivate(), state=CalculateClothes.photo, content_types=ContentType.PHOTO)
async def get_clothes_photo(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "Назад ↩️":
        await state.finish()
        await menu(message)
        return

    if not message.photo:
        await message.answer("Неверный формат ввода.\n"
                             "Отправьте скриншот, на котором будет видно: Товар, размер, цвет.")
        await CalculateClothes.photo.set()

    photo = await get_photo(message)
    await state.update_data(photo=photo)

    data = await state.get_data()

    order_number = await create_an_order_number()
    user_id = message.from_user.id
    order_name = data.get("order_name")
    link = data.get("link")
    status = "создан"
    price = data.get("price")
    photo = data.get("photo")

    ORDERS.append_row([order_number, user_id, order_name, link, status, price, photo])

    text = ""
    text += (f"#{order_number}\n"
             f"\t\t\t\t username:\t\t@{message.from_user.username}\n"
             f"\t\t\t\t Название:\t\t{order_name}\n"
             f"\t\t\t\t Статус:\t\t{status}\n"
             f"\t\t\t\t Стоимость:\t\t{price} руб\n"
             f"\t\t\t\t Ссылка: \t\t{link}")
    await bot.send_message(473151013, f"Новый заказ (одежда).\n{text}")

    await message.answer(f"Заказ #{order_number} создан и отправлен модератору. В ближайшее время он будет рассмотрен")

    await menu(message)
    await state.finish()
