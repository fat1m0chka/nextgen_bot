from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu(is_admin=False):

    keyboard = [
        [
            KeyboardButton(text="🎮 Привязать аккаунт")
        ],
        [
            KeyboardButton(text="🪙 Мои токены"),
            KeyboardButton(text="🏆 Результаты")
        ]
    ]

    if is_admin:
        keyboard.append(
            [
                KeyboardButton(text="🛠 Админ панель")
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )