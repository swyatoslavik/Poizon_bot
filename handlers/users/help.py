from aiogram import types
from aiogram.types import MediaGroup, InputFile

from loader import dp


@dp.message_handler(text="/help")
async def command_help(message: types.Message):
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

                         "Если у вас возникнут какие-либо вопросы, пожалуйста, воспользуйтесь кнопкой '👨‍💻Помощь'. Мы всегда готовы помочь вам с выбором товара и ответить на любые вопросы. Спасибо, что выбрали наш сервис 🤗")

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