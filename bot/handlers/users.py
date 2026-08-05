from aiogram import Router
from aiogram.types import Message

from database.crud import get_users

router = Router()


@router.message(lambda m: m.text == "👥 Пользователи")
async def users(message: Message):

    users = await get_users()

    if not users:
        await message.answer("Пользователей нет.")
        return

    text = "👥 Пользователи\n\n"

    for user in users:

        text += (
            f"🎮 {user.nickname}\n"
            f"📱 {user.phone}\n"
            f"🪙 {user.tokens}\n"
            f"📌 {user.status}\n\n"
        )

    await message.answer(text)