from aiogram import Router
from aiogram.types import Message

from bot.keyboards.main import main_menu
from bot.keyboards.admin import admin_menu
from bot.keyboards.contest import contest_menu

from bot.utils.admin import is_channel_admin
from config.settings import settings


router = Router()


@router.message(lambda message: message.text == "⬅️ Назад")
async def back_handler(message: Message):

    admin = await is_channel_admin(
        message.bot,
        settings.CHANNEL_ID,
        message.from_user.id
    )

    await message.answer(
        "👋 Главное меню",
        reply_markup=main_menu(admin)
    )