from aiogram import Router
from aiogram.types import CallbackQuery

from config.settings import settings
from bot.utils.check_subscription import check_subscription
from bot.keyboards.main import main_menu


router = Router()


@router.callback_query(lambda c: c.data == "check_sub")
async def check(callback: CallbackQuery):

    result = await check_subscription(
        callback.bot,
        callback.from_user.id,
        settings.CHANNEL_ID
    )

    if result:
        await callback.message.edit_text(
            "✅ Подписка подтверждена!"
        )

        await callback.message.answer(
            "Главное меню:",
            reply_markup=main_menu
        )

    else:
        await callback.answer(
            "❌ Вы еще не подписались",
            show_alert=True
        )