from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_select_change = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💭Изменить название"),
            KeyboardButton(text="🔄Изменить статус"),
            KeyboardButton(text="💰Изменить стоимость"),
        ],
        [
            KeyboardButton(text="🔗Изменить ссылку"),
            KeyboardButton(text="📷Изменить фотографию"),
        ],
        [
            KeyboardButton(text="Назад ↩️"),
        ]
    ],
    resize_keyboard=True
)
