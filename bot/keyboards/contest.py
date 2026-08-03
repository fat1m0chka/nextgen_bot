from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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