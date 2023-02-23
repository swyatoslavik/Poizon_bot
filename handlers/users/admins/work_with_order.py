from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext

import urllib.request

from data.config import admins_id

from google_sheets import ORDERS

from handlers.users.admins.admins_menu import menu

from keyboards.default import kb_statuses, admins_menu, kb_return
from loader import dp
from states.admins import ChangeOrderStatus


async def send_image(chat_id: int, image_url: str, caption: str = None):
    with urllib.request.urlopen(image_url) as url:
        content_type = url.info().get_content_type()
        if content_type.startswith('image/'):
            image_bytes = BytesIO(url.read())
            photo = types.InputFile(image_bytes, filename='image.jpg')
            return photo
        elif content_type == 'application/octet-stream':
            # Check file header or signature to determine file type
            file_header = url.read(16)
            if file_header.startswith(b'\xff\xd8'):
                # JPEG file
                image_bytes = BytesIO(file_header + url.read())
                photo = types.InputFile(image_bytes, filename='image.jpg')
                return photo
            elif file_header.startswith(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'):
                # PNG file
                image_bytes = BytesIO(file_header + url.read())
                photo = types.InputFile(image_bytes, filename='image.png')
                return photo
            else:
                raise TypeError('Unsupported file type.')
        else:
            raise TypeError('Not an image file.')


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
             f"\t\t\t\t Стоимость:\t\t{order_info[5]} руб\n\n"
             f"\t\t\t\t Ссылка:\t\t{order_info[4]}")
    photo = await send_image(chat_id=message.chat.id, image_url=order_info[6])
    await message.answer(text, reply_markup=kb_statuses)
    await dp.bot.send_photo(message.from_user.id, photo=photo)
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
    await message.answer("Данные успешно обновлены.", reply_markup=admins_menu)
    order_info = ORDERS.row_values(ORDERS.find(data.get("select_order")).row)
    user = await dp.bot.get_chat(order_info[1])
    text = ""
    text += (f"#{order_info[0]}\n"
             f"\t\t\t\t username:\t\t@{user.username}\n"
             f"\t\t\t\t Название:\t\t{order_info[2]}\n"
             f"\t\t\t\t Статус:\t\t{order_info[4]}\n"
             f"\t\t\t\t Стоимость:\t\t{order_info[5]} руб\n\n"
             f"\t\t\t\t Ссылка:\t\t{order_info[4]}")
    await message.answer(text)

    await dp.bot.send_message(int(ORDERS.cell(ORDERS.find(data.get("select_order")).row, 2).value),
                              f"Ваш заказ #{data.get('select_order')} получил новый статус: {answer}")

    await state.finish()
