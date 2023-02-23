from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да ️✅"),
            KeyboardButton(text="Нет❌️"),
        ],
        [
            KeyboardButton(text="Назад ↩️"),
        ]
    ],
    resize_keyboard=True
)
