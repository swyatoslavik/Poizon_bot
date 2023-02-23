from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeCourse(StatesGroup):
    new_num = State()


class ChangeShoes(StatesGroup):
    new_num = State()


class ChangeClothes(StatesGroup):
    new_num = State()


class ChangeCommission(StatesGroup):
    new_num = State()

class ChangeOrderStatus(StatesGroup):
    select_order = State()
    change_status = State()