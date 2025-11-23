from aiogram.fsm.state import StatesGroup, State


class CreateTicket(StatesGroup):
    analysis = State()
    day = State()
    device = State()
    executor = State()
    quantity = State()
    confirm = State()


class RateTicket(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    confirm = State()
