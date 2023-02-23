from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeAnOrder(StatesGroup):
    type = State()

