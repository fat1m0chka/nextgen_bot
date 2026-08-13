from aiogram import Router
from aiogram.types import Message

from database.crud import get_user

router = Router()


@router.message(lambda m: m.text == "👤 Мой профиль")
async def profile(message: Message):

    user = await get_user(
        message.from_user.id
    )

    if not user:
        await message.answer(
            "❌ Вы еще не зарегистрированы"
        )
        return


    await message.answer(
        f"👤 Ваш профиль\n\n"
        f"🆔 ID: {user.telegram_id}\n"
        f"👤 Telegram: @{user.telegram_username or 'нет'}\n\n"
        f"🎮 Ник: {user.nickname or 'не указан'}\n"
        f"📱 Телефон: {user.phone or 'не указан'}\n\n"
        f"🪙 Токены: {user.tokens}\n\n"
        f"📌 Статус: {user.status}"
    )