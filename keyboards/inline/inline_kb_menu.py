from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Обувь",
                                                             callback_data="Обувь"),
                                        InlineKeyboardButton(text="Одежда/аксессуары",
                                                             callback_data="Одежда/аксессуары")
                                    ],
                                ])
