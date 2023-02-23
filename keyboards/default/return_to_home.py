from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_return = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад ↩️"),
        ]
    ],
    resize_keyboard=True
)
