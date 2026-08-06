from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def user_menu(is_admin=False):

    keyboard = [
        [KeyboardButton(text="🎁 Активные конкурсы")],
        [
            KeyboardButton(text="🪙 Мои токены"),
            KeyboardButton(text="🏆 Победители")
        ],
        [
            KeyboardButton(text="📜 История")
        ]
    ]

    if is_admin:
        keyboard.append(
            [KeyboardButton(text="🛠 Админ панель")]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def main_menu(is_admin=False):

    keyboard = [
        [KeyboardButton(text="🎮 Привязать аккаунт")],
        [
            KeyboardButton(text="🪙 Мои токены"),
            KeyboardButton(text="🏆 Результаты")
        ]
    ]

    if is_admin:
        keyboard.append(
            [KeyboardButton(text="🛠 Админ панель")]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )