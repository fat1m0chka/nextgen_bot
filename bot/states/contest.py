from aiogram.fsm.state import State, StatesGroup

class ContestState(StatesGroup):
    photo = State()
    title = State()
    description = State()
    prize = State()

    date = State()
    time = State()