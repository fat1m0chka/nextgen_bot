from aiogram.fsm.state import State, StatesGroup

class TokenState(StatesGroup):
    user = State()
    amount = State()