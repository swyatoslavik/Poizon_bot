from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_statuses = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="принят"),
            KeyboardButton(text="оплачен"),
            KeyboardButton(text="выкуплен"),

        ],
        [
            KeyboardButton(text="отправлен продавцом"),
            KeyboardButton(text="на складе Poison"),
            KeyboardButton(text="на складе службы доставки"),
            KeyboardButton(text="отправлен в Россию"),
        ],
        [
            KeyboardButton(text="прибыл в Уссурийск"),
            KeyboardButton(text="отправлен к PoisonSell"),
            KeyboardButton(text="принят PoisonSell"),
        ],
        [
            KeyboardButton(text="отправлен покупателю"),
            KeyboardButton(text="завершён"),
        ],
        [
            KeyboardButton(text="Назад ↩️"),
        ]
    ],
    resize_keyboard=True
)
