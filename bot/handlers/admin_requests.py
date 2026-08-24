from aiogram import Router
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from bot.loader import bot
from database.crud import get_active_admins_ids
from config.settings import settings

from database.crud import (
    get_pending_requests,
    get_user_by_id,
    update_status
)

router = Router()


# =========================================================
# КЛАВИАТУРА ЗАЯВКИ
# =========================================================

def request_keyboard(user_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Одобрить",
                    callback_data=f"approve_{user_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_{user_id}"
                )
            ]
        ]
    )


# =========================================================
# СПИСОК ЗАЯВОК
# =========================================================

@router.message(
    lambda m: m.text == "📋 Заявки"
)
async def requests(message: Message):

    users = await get_pending_requests()

    if not users:
        await message.answer(
            "📭 Новых заявок нет"
        )
        return

    for user in users:

        await message.answer(
            f"""
📋 <b>Заявка #{user.id}</b>

👤 <b>Telegram:</b>
{user.telegram_username or "нет"}

🎮 <b>Ник:</b>
{user.nickname or "не указан"}

📱 <b>Телефон:</b>
{user.phone or "не указан"}
            """,
            reply_markup=request_keyboard(user.id),
            parse_mode="HTML"
        )


# =========================================================
# НОВАЯ ЗАЯВКА → УВЕДОМЛЕНИЕ АДМИНУ
# =========================================================

async def notify_new_request(user_id: int):
    # Достаем инфу о юзере из БД
    user = await get_user_by_id(user_id)
    
    if not user:
        return

    # Формируем текст (теги <code> позволят админу скопировать номер/ник по клику)
    text = (
        f"🔔 <b>Новая заявка (ID: {user.id})</b>\n\n"
        f"🎮 Ник: <code>{user.nickname or 'не указан'}</code>\n"
        f"📱 Телефон: <code>{user.phone or 'не указан'}</code>"
    )

    try:
        admins = await bot.get_chat_administrators(settings.CHANNEL_ID)
        
        for admin in admins:
            if admin.user.is_bot:
                continue
            
            try:
                await bot.send_message(
                    chat_id=admin.user.id,
                    text=text,
                    reply_markup=request_keyboard(user.id),
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Не удалось отправить в ЛС админу {admin.user.id}: {e}")
                
    except Exception as e:
        print(f"Ошибка получения списка админов канала: {e}")


# =========================================================
# ОДОБРЕНИЕ
# =========================================================

@router.callback_query(
    lambda c: c.data.startswith("approve_")
)
async def approve_user(callback: CallbackQuery):

    user_id = int(
        callback.data.split("_")[1]
    )

    user = await get_user_by_id(user_id)

    if not user:

        await callback.answer(
            "❌ Пользователь не найден.",
            show_alert=True
        )
        return

    # Проверяем ДО изменения статуса
    if user.status == "approved":

        await callback.answer(
            "⚠️ Пользователь уже одобрен.",
            show_alert=True
        )
        return

    if user.status != "pending":

        await callback.answer(
            "⚠️ Эта заявка уже обработана.",
            show_alert=True
        )
        return

    # Меняем статус
    await update_status(
        user_id,
        "approved"
    )

    # Уведомляем пользователя
    try:

        await bot.send_message(
            user.telegram_id,
            "🎉 <b>Ваша заявка одобрена!</b>\n\n"
            "Теперь вам доступны:\n"
            "🎁 Участие в конкурсах\n"
            "🪙 Использование токенов\n"
            "🏆 Просмотр результатов\n\n"
            "Нажмите /start для обновления меню.",
            parse_mode="HTML"
        )

    except Exception as e:

        print(
            f"Не удалось отправить уведомление "
            f"{user.telegram_id}: {e}"
        )

    # Меняем сообщение админу
    await callback.message.edit_text(
        callback.message.text +
        "\n\n✅ <b>Пользователь одобрен</b>",
        parse_mode="HTML"
    )

    await callback.answer(
        "✅ Пользователь одобрен"
    )


# =========================================================
# ОТКЛОНЕНИЕ
# =========================================================

@router.callback_query(
    lambda c: c.data.startswith("reject_")
)
async def reject(callback: CallbackQuery):

    user_id = int(
        callback.data.split("_")[1]
    )

    user = await get_user_by_id(user_id)

    if not user:

        await callback.answer(
            "❌ Пользователь не найден.",
            show_alert=True
        )
        return

    if user.status != "pending":

        await callback.answer(
            "⚠️ Эта заявка уже обработана.",
            show_alert=True
        )
        return

    await update_status(
        user_id,
        "rejected"
    )

    # Уведомляем пользователя
    try:

        await bot.send_message(
            user.telegram_id,
            "❌ <b>Ваша заявка отклонена.</b>\n\n"
            "Если вы считаете, что это ошибка, "
            "обратитесь к администратору.",
            parse_mode="HTML"
        )

    except Exception as e:

        print(
            f"Не удалось отправить уведомление "
            f"{user.telegram_id}: {e}"
        )

    await callback.message.edit_text(
        "❌ <b>Пользователь отклонен</b>",
        parse_mode="HTML"
    )

    await callback.answer(
        "❌ Заявка отклонена"
    )