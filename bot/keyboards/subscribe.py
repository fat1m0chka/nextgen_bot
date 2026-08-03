from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def subscribe_keyboard(channel):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Канал",
                    url=f"https://t.me/{channel}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Проверить подписку",
                    callback_data="check_sub"
                )
            ]
        ]
    )