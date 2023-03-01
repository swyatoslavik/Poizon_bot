from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeCourse(StatesGroup):
    new_num = State()


class ChangeShoes(StatesGroup):
    new_num = State()


class ChangeClothes(StatesGroup):
    new_num = State()


class ChangeCommission(StatesGroup):
    new_num = State()


class ChangeOrder(StatesGroup):
    order_number = State()
    type_of_change = State()
    final = State()


class ChangeOrderName(StatesGroup):
    new_order_name = State()


class ChangeOrderStatus(StatesGroup):
    select_order = State()
    change_status = State()


class AddPromocode(StatesGroup):
    promocode = State()
