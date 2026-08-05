from aiogram import Router
from aiogram.types import Message

from database.crud import get_statistics

router = Router()


@router.message(lambda m: m.text == "📊 Статистика")
async def stats(message: Message):

    s = await get_statistics()

    await message.answer(
        f"""
📊 Статистика

👥 Всего пользователей:
{s["total"]}

✅ Подтверждено:
{s["approved"]}

🕒 Ожидают:
{s["pending"]}

❌ Отклонено:
{s["rejected"]}

🪙 Всего токенов:
{s["tokens"]}
"""
    )