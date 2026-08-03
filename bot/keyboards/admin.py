from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 Заявки")
        ],
        [
            KeyboardButton(text="🎁 Конкурсы")
        ],
        [
            KeyboardButton(text="👥 Пользователи"),
            KeyboardButton(text="📊 Статистика")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)