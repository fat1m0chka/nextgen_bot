from aiogram import Router
from aiogram.types import CallbackQuery

from bot.keyboards.main import main_menu
from bot.utils.check_subscription import check_subscription
from bot.utils.admin import is_channel_admin
from config.settings import settings


router = Router()


@router.callback_query(lambda c: c.data == "check_sub")
async def check_sub(callback: CallbackQuery):

    user_id = callback.from_user.id


    subscribed = await check_subscription(
        callback.bot,
        user_id,
        settings.CHANNEL_ID
    )


    if not subscribed:
        await callback.answer(
            "❌ Вы еще не подписались",
            show_alert=True
        )
        return


    admin = await is_channel_admin(
        callback.bot,
        settings.CHANNEL_ID,
        user_id
    )


    await callback.message.edit_text(
        "👋 Добро пожаловать!\n\n"
        "Выберите действие:"
    )


    await callback.message.answer(
        "Меню:",
        reply_markup=main_menu(admin)
    )