from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_return_to_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏠Главное меню"),
        ]
    ],
    resize_keyboard=True
)
