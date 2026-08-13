from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.loader import bot
from database.crud import get_pending_requests
from database.crud import get_user_by_id


router = Router()


@router.message(lambda m: m.text == "📋 Заявки")
async def requests(message: Message):

    users = await get_pending_requests()

    if not users:
        await message.answer(
            "📭 Новых заявок нет"
        )
        return


    for user in users:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Одобрить",
                        callback_data=f"approve_{user.id}"
                    ),
                    InlineKeyboardButton(
                        text="❌ Отклонить",
                        callback_data=f"reject_{user.id}"
                    )
                ]
            ]
        )


        await message.answer(
            f"""
📋 Заявка #{user.id}

👤 Telegram:
{user.telegram_username}

🎮 Ник:
{user.nickname}

📱 Телефон:
{user.phone}
            """,
            reply_markup=keyboard
        )


from aiogram.types import CallbackQuery
from database.crud import update_status


@router.callback_query(lambda c: c.data.startswith("approve_"))
async def approve_user(callback: CallbackQuery):

    user_id = int(
        callback.data.split("_")[1]
    )

    user = await get_user_by_id(user_id)

    await update_status(
        user_id,
        "approved"
    )

    if user.status == "approved":
        await callback.answer(
            "Пользователь уже одобрен",
            show_alert=True
        )
        return

    try:
        await bot.send_message(
            user.telegram_id,
            "🎉 Ваш аккаунт одобрен!\n\n"
            "Теперь вам доступны:\n"
            "🎁 Участие в конкурсах\n"
            "🪙 Использование токенов\n"
            "🏆 Просмотр результатов\n\n"
            "Нажмите /start для обновления меню."
)

    except Exception as e:
        print(e)

    await callback.message.edit_text(
        callback.message.text + "\n\n✅ Пользователь одобрен"
    )


@router.callback_query(lambda c: c.data.startswith("reject_"))
async def reject(callback: CallbackQuery):

    user_id = int(
        callback.data.split("_")[1]
    )

    await update_status(
        user_id,
        "rejected"
    )

    await callback.message.edit_text(
        "❌ Пользователь отклонен"
    )