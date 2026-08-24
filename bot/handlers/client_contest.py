from aiogram import Router
from aiogram.types import Message, CallbackQuery

from database.crud_contest import (
    get_all_contests,
    join_contest
)

from bot.keyboards.client_contest import contest_join


router = Router()


# =========================
# КЛИЕНТ: КОНКУРСЫ
# =========================

@router.message(lambda m: m.text == "🎁 Конкурсы")
async def client_contests(message: Message):

    contests = await get_all_contests()

    active_contests = [
        contest
        for contest in contests
        if contest.status == "active"
    ]

    if not active_contests:
        await message.answer(
            "🎁 Сейчас активных конкурсов нет."
        )
        return

    for contest in active_contests:

        await message.answer_photo(
            photo=contest.photo_id,
            caption=(
                f"🏆 <b>{contest.title}</b>\n\n"
                f"🎁 <b>Приз:</b> {contest.prize}\n\n"
                f"📝 <b>Условия:</b>\n"
                f"{contest.description}\n\n"
                f"🕓 <b>Проведение:</b>\n"
                f"{contest.start_at}\n\n"
                f"🟢 <b>Статус:</b> Активен"
            ),
            reply_markup=contest_join(contest.id),
            parse_mode="HTML"
        )


# =========================
# УЧАСТИЕ
# =========================

@router.callback_query(
    lambda c: c.data.startswith("join_")
)
async def join_contest_handler(
    callback: CallbackQuery
):

    contest_id = int(
        callback.data.split("_")[-1]
    )

    result = await join_contest(
        contest_id=contest_id,
        telegram_id=callback.from_user.id
    )

    if result == "not_registered":

        await callback.answer(
            "❌ Вы ещё не зарегистрированы.",
            show_alert=True
        )
        return

    if result == "not_approved":

        await callback.answer(
            "⏳ Ваш аккаунт ещё не одобрен.",
            show_alert=True
        )
        return

    if result == "no_tokens":

        await callback.answer(
            "❌ Для участия нужен хотя бы 1 токен.",
            show_alert=True
        )
        return

    if result == "contest_not_found":

        await callback.answer(
            "❌ Конкурс не найден.",
            show_alert=True
        )
        return

    if result == "contest_finished":

        await callback.answer(
            "🔴 Этот конкурс уже завершён.",
            show_alert=True
        )
        return

    if result == "already_joined":

        await callback.answer(
            "⚠️ Вы уже участвуете в этом конкурсе.",
            show_alert=True
        )
        return

    if result == "joined":

        await callback.answer(
            "🎉 Вы участвуете!",
            show_alert=True
        )

        await callback.message.answer(
            "🎉 <b>Вы успешно участвуете в конкурсе!</b>\n\n"
            "Удачи! 🍀\n\n"
            "ℹ️ Токены за участие не списываются.",
            parse_mode="HTML"
        )

        return