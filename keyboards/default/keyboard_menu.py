from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💰Рассчитать обувь"),
        ],
        [
            KeyboardButton(text="💰Рассчитать одежду/аксессуары"),
        ],
        [
            KeyboardButton(text="🎯Отзывы"),
            KeyboardButton(text="👨‍💻Помощь"),
        ],
        [
            KeyboardButton(text="🚚Заказать"),
            KeyboardButton(text="📋Мои заказы"),
        ]
    ],
    resize_keyboard=True
)
