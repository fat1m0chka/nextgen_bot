from aiogram import Router
from aiogram.types import Message

from bot.keyboards.admin import admin_menu
from bot.utils.admin import is_channel_admin
from config.settings import settings


router = Router()


@router.message(lambda message: message.text == "🛠 Админ панель")
async def admin_panel(message: Message):

    check = await is_channel_admin(
        message.bot,
        settings.CHANNEL_ID,
        message.from_user.id
    )

    if not check:
        await message.answer(
            "❌ Нет доступа"
        )
        return

    await message.answer(
        "🛠 Админ панель\n\n"
        "Выберите действие:",
        reply_markup=admin_menu
    )