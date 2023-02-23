from aiogram.dispatcher.filters.state import StatesGroup, State


class CalculateClothes(StatesGroup):
    price = State()
    status = State()
    order_name = State()
    link = State()
    photo = State()
