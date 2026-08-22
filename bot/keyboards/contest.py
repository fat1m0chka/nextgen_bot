from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

contest_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="➕ Создать конкурс"
            )
        ],
        [
            KeyboardButton(
                text="📋 Список конкурсов"
            )
        ],
        [
            KeyboardButton(
                text="⬅️ Назад"
            )
        ]
    ],
    resize_keyboard=True
)

def contest_admin_menu(contest_id: int):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="⏹ Завершить досрочно",
        callback_data=f"finish_contest_{contest_id}"
    )

    return builder.as_markup()