from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    nickname = State()
    phone = State()