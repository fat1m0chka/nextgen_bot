from aiogram.fsm.state import State, StatesGroup

from database.crud import (
    get_user_by_phone,
    add_tokens
)

class TokenState(StatesGroup):
    user = State()
    amount = State()