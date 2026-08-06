from aiogram.utils.keyboard import InlineKeyboardBuilder

def contest_join(contest_id):

    kb = InlineKeyboardBuilder()

    kb.button(
        text="🎉 Участвовать",
        callback_data=f"join_{contest_id}"
    )

    return kb.as_markup()