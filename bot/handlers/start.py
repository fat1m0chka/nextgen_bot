from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.subscribe import subscribe_keyboard
from bot.utils.check_subscription import check_subscription
from config.settings import settings
from bot.keyboards.main import main_menu
from bot.utils.admin import is_channel_admin
from database.crud import get_user
from bot.keyboards.main import main_menu, user_menu

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    is_subscribed = await check_subscription(
        message.bot,
        message.from_user.id,
        settings.CHANNEL_ID
    )

    if not is_subscribed:
        await message.answer(
            "❌ Для участия в конкурсе подпишитесь на канал:",
            reply_markup=subscribe_keyboard(
                settings.CHANNEL_USERNAME
            )
        )
        return

    admin = await is_channel_admin(
        message.bot,
        settings.CHANNEL_ID,
        message.from_user.id
    )

    user = await get_user(message.from_user.id)

    if user and user.status == "approved":
        keyboard = user_menu(admin)
    else:
        keyboard = main_menu(admin)

    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "🎁 Здесь вы можете участвовать в конкурсах и получать токены.",
        reply_markup=keyboard
    )
