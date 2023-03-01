from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admins_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💴Изменить курс юаня"),

        ],
        [
            KeyboardButton(text="👟Изменить обувь"),
            KeyboardButton(text="👔Изменить одежду/аксы"),
            KeyboardButton(text="💰Изменить комиссию"),
        ],
        [
            KeyboardButton(text="📋Список заказов"),
            KeyboardButton(text="🔄Обработать заказ"),
        ],
        [
            KeyboardButton(text="🎟Добавить промокод"),
        ],
        [
            KeyboardButton(text="🏠Главное меню"),
        ]
    ],
    resize_keyboard=True
)
