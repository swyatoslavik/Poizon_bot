from aiogram import types
from aiogram.types import CallbackQuery, MediaGroup, InputFile

from google_sheets import ORDERS
from handlers.users.menu import menu
from keyboards.default import kb_return
from keyboards.inline import ikb_menu
from loader import dp
from states.calculate_clothes import CalculateClothes
from states.calculate_shoes import CalculateShoes


@dp.message_handler(text="💰Рассчитать обувь")
async def command_calculate_shoes(message: types.Message):
    await message.answer("Укажите стоимость товара в юанях", reply_markup=kb_return)
    await CalculateShoes.price.set()


@dp.message_handler(text="💰Рассчитать одежду/аксессуары")
async def command_calculate_clothes(message: types.Message):
    await message.answer("Укажите стоимость товара в юанях", reply_markup=kb_return)
    await CalculateClothes.price.set()


@dp.message_handler(text="🎯Отзывы")
async def command_reviews(message: types.Message):
    await message.answer("Отзывы")


@dp.message_handler(text="👨‍💻Помощь")
async def command_connect_with_manager(message: types.Message):
    await message.answer(f"Как оформить заказ? 🤔\n\n"

                         "<b>1.</b> Установите приложение Poison (Dewu) 📲\n"
                         "<b>2.</b> Зайдите в приложение и выберите товар, который вам нравится. 🛍\n"
                         "<b>3.</b> Проверьте, есть ли нужный вам размер у продавца и посмотрите цену (см. скриншот 1) 😎\n"
                         "<b>4.</b> Перейдите в бота @Poison_sellBot и начните оформление заказа. Для этого в главном меню нажмите на кнопку \n'🚚Заказать' (см. скриншот 2.1) 💬\n"
                         "<b>5.</b> Выберите тип вашего товара с помощью инлайн кнопок (см. скриншот 2.2) 🤖\n"
                         "<b>6.</b> Укажите цену на товар в юанях, указанную в пункте 3 💰\n"
                         "<b>7.</b> Придумайте название вашего заказа, которое должно содержать название товара, размер и цвет 📝\n"
                         "<b>8.</b> Укажите ссылку на товар из приложения Poison (Dewu) (см. скриншоты 3 и 4) 🔗\n"
                         "<b>9.</b> Пришлите скриншот, на котором будет видно размер, цвет и цену вашего товара (см. скриншот 5) 📷\n\n"
                         "Пожалуйста, внимательно отнеситесь к каждому пункту для корректного оформления заказа. Если вы всё сделали правильно, бот укажет вам номер вашего заказа и отправит его модераторам на проверку. 🙌\n\n"

                         "Если у вас возникнут какие-либо вопросы, пожалуйста, воспользуйтесь кнопкой '👨‍💻Помощь'. Мы всегда готовы помочь вам с выбором товара и ответить на любые вопросы. Спасибо, что выбрали наш сервис 🤗"
                         "❔Менеджер/Тех.Поддержка —  @poison_sell_manager")

    album = MediaGroup()
    photo_bytes = InputFile(path_or_bytesio="media/Photo1.jpg")
    album.attach_photo(photo=photo_bytes)
    photo_bytes = InputFile(path_or_bytesio="media/Photo2.1.jpg")
    album.attach_photo(photo=photo_bytes)
    photo_bytes = InputFile(path_or_bytesio="media/Photo2.2.jpg")
    album.attach_photo(photo=photo_bytes)
    photo_bytes = InputFile(path_or_bytesio="media/Photo3.jpg")
    album.attach_photo(photo=photo_bytes)
    photo_bytes = InputFile(path_or_bytesio="media/Photo4.jpg")
    album.attach_photo(photo=photo_bytes)
    photo_bytes = InputFile(path_or_bytesio="media/Photo5.jpg")
    album.attach_photo(photo=photo_bytes)
    await message.answer_media_group(album)


@dp.message_handler(text="🚚Заказать")
async def show_inline_menu_to_choose_order_type(message: types.Message):
    await message.answer("Выберите категорию товара:", reply_markup=ikb_menu)


@dp.callback_query_handler(text="Обувь")
async def select_type_of_order_shoes(callback_query: CallbackQuery):
    await callback_query.message.answer("Укажите стоимость товара в юанях", reply_markup=kb_return)
    await CalculateShoes.price.set()


@dp.callback_query_handler(text="Одежда/аксессуары")
async def select_type_of_order_clothes(callback_query: CallbackQuery):
    await callback_query.message.answer("Укажите стоимость товара в юанях", reply_markup=kb_return)
    await CalculateClothes.price.set()


@dp.message_handler(text="📋Мои заказы")
async def command_faq(message: types.Message):
    list_of_dicts = ORDERS.get_all_records()
    list_of_orders = []
    for slovar in list_of_dicts:
        if str(slovar["user_id"]) == str(message.from_user.id):
            list_of_orders.append([slovar["order_number"],
                                   slovar["order_name"],
                                   slovar["status"],
                                   slovar["price"],
                                   slovar["link"]])
    text = ""
    for order in list_of_orders:
        text += (f"#{order[0]}\n"
                 f"\t\t\t\t Название:\t\t{order[1]}\n"
                 f"\t\t\t\t Статус:\t\t{order[2]}\n"
                 f"\t\t\t\t Стоимость:\t\t{order[3]} руб\n\n"
                 f"\t\t\t\t Ссылка: \t\t{order[4]}")
    await message.answer(text)


@dp.message_handler(text="Назад ↩️")
async def command_back(message: types.Message):
    await menu(message)
