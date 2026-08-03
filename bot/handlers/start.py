from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.keyboards.subscribe import subscribe_keyboard
from bot.utils.check_subscription import check_subscription
from config.settings import settings
from bot.keyboards.main import main_menu
from bot.utils.admin import is_channel_admin

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
        reply_markup=subscribe_keyboard(settings.CHANNEL_ID)
)
        return

    admin = await is_channel_admin(
    message.bot,
    settings.CHANNEL_ID,
    message.from_user.id
)
    print(
    "ADMIN CHECK:",
    message.from_user.id,
    admin
)

    await message.answer(
    "👋 Добро пожаловать!\n\n"
    "🎁 Здесь вы можете участвовать в конкурсах "
    "и получать токены.",
    reply_markup=main_menu(admin)
)