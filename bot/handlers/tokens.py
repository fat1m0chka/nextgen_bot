from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.crud import get_user_by_phone

from bot.states.tokens import TokenState

router = Router()


@router.message(lambda m: m.text == "🪙 Выдать токены")
async def start_tokens(message: Message, state: FSMContext):

    await state.set_state(TokenState.user)

    await message.answer(
        "Введите номер телефона пользователя"
    )


from database.crud import get_user_by_phone

@router.message(TokenState.user)
async def get_user(message: Message, state: FSMContext):

    phone = message.text.strip()

    user = await get_user_by_phone(phone)

    if not user:
        await message.answer(
            "❌ Пользователь с таким номером не найден."
        )
        return

    await state.update_data(
        user_id=user.id
    )

    await state.set_state(
        TokenState.amount
    )

    await message.answer(
        f"👤 Пользователь: {user.nickname}\n"
        f"📱 {user.phone}\n\n"
        "💰 Введите сумму пополнения в рублях:"
    )


@router.message(TokenState.amount)
async def get_amount(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer(
            "Введите только число."
        )
        return

    amount = int(message.text)

    tokens = amount // 1000

    data = await state.get_data()

    user = await add_tokens(
        data["user_id"],
        tokens
    )

    await message.answer(
        f"""
✅ Токены начислены

👤 {user.nickname}
📱 {user.phone}

💰 Пополнение: {amount} ₽

🪙 Начислено: {tokens}

💎 Всего токенов:
{user.tokens}
"""
    )

    await state.clear()