from datetime import datetime

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states.contest import ContestState
from bot.keyboards.client_contest import contest_join
from bot.keyboards.contest import contest_menu, contest_admin_menu

from database.crud_contest import (
    create_contest,
    get_all_contests,
    get_contest,
    join_contest,
    is_joined,
    finish_contest
)


router = Router()


# =========================
# АДМИН: КОНКУРСЫ
# =========================

@router.message(
    lambda m: m.text == "🎁 Конкурсы"
)
async def contest_start(message: Message):

    await message.answer(
        "🎁 Управление конкурсами:",
        reply_markup=contest_menu
    )


# =========================
# СОЗДАНИЕ
# =========================

@router.message(
    lambda m: m.text == "➕ Создать конкурс"
)
async def create_start(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        ContestState.photo
    )

    await message.answer(
        "📸 Отправьте картинку конкурса"
    )


@router.message(
    ContestState.photo
)
async def get_photo(
    message: Message,
    state: FSMContext
):

    if not message.photo:

        await message.answer(
            "Нужна именно картинка"
        )

        return

    await state.update_data(
        photo_id=message.photo[-1].file_id
    )

    await state.set_state(
        ContestState.title
    )

    await message.answer(
        "✏️ Название конкурса:"
    )


@router.message(
    ContestState.title
)
async def get_title(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        title=message.text
    )

    await state.set_state(
        ContestState.description
    )

    await message.answer(
        "📝 Условия конкурса:"
    )


@router.message(
    ContestState.description
)
async def get_desc(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        description=message.text
    )

    await state.set_state(
        ContestState.prize
    )

    await message.answer(
        "🏆 Приз:"
    )


@router.message(
    ContestState.prize
)
async def get_prize(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        prize=message.text
    )

    await state.set_state(
        ContestState.date
    )

    await message.answer(
        "📅 Введите дату проведения\n\n"
        "Пример:\n"
        "08.08.2026"
    )


@router.message(
    ContestState.date
)
async def get_date(
    message: Message,
    state: FSMContext
):

    try:
        datetime.strptime(
            message.text,
            "%d.%m.%Y"
        )

    except ValueError:

        await message.answer(
            "Неверный формат.\n\n"
            "Пример: 08.08.2026"
        )

        return

    await state.update_data(
        date=message.text
    )

    await state.set_state(
        ContestState.time
    )

    await message.answer(
        "🕓 Введите время\n\n"
        "Пример:\n"
        "18:30"
    )


@router.message(
    ContestState.time
)
async def get_time(
    message: Message,
    state: FSMContext
):

    try:
        datetime.strptime(
            message.text,
            "%H:%M"
        )

    except ValueError:

        await message.answer(
            "Неверное время.\n\n"
            "Пример: 18:30"
        )

        return

    data = await state.get_data()

    start_at = (
        f'{data["date"]} {message.text}'
    )

    end_at = (
        f'{data["date"]} 23:59'
    )

    await create_contest(
        photo_id=data["photo_id"],
        title=data["title"],
        description=data["description"],
        prize=data["prize"],
        start_at=start_at,
        end_at=end_at
    )

    await message.answer(
        "✅ Конкурс создан!",
        reply_markup=contest_menu
    )

    await state.clear()


# =========================
# АДМИН: СПИСОК
# =========================

@router.message(
    lambda m: m.text == "📋 Список конкурсов"
)
async def contests_list(message: Message):

    contests = await get_all_contests()

    if not contests:

        await message.answer(
            "📭 Конкурсов пока нет."
        )

        return

    for contest in contests:

        if contest.status == "finished":

            caption = (
                f"🏆 <b>{contest.title}</b>\n\n"
                f"🎁 <b>Приз:</b> {contest.prize}\n\n"
                f"📝 <b>Условия:</b>\n"
                f"{contest.description}\n\n"
                f"🔴 <b>Статус: Завершён</b>"
            )

            await message.answer_photo(
                photo=contest.photo_id,
                caption=caption,
                parse_mode="HTML"
            )

        else:

            caption = (
                f"🏆 <b>{contest.title}</b>\n\n"
                f"🎁 <b>Приз:</b> {contest.prize}\n\n"
                f"📝 <b>Условия:</b>\n"
                f"{contest.description}\n\n"
                f"🟢 <b>Статус: Активен</b>"
            )

            await message.answer_photo(
                photo=contest.photo_id,
                caption=caption,
                reply_markup=contest_admin_menu(
                    contest.id
                ),
                parse_mode="HTML"
            )


# =========================
# ДОСРОЧНОЕ ЗАВЕРШЕНИЕ
# =========================

@router.callback_query(
    lambda c: c.data.startswith(
        "finish_contest_"
    )
)
async def finish_contest_handler(
    callback: CallbackQuery
):

    contest_id = int(
        callback.data.split("_")[-1]
    )

    result = await finish_contest(
        contest_id
    )

    if result == "not_found":

        await callback.answer(
            "❌ Конкурс не найден.",
            show_alert=True
        )

        return

    if result == "already_finished":

        await callback.answer(
            "⚠️ Конкурс уже завершён.",
            show_alert=True
        )

        return

    if result == "no_participants":

        await callback.answer(
            "Конкурс завершён, участников нет.",
            show_alert=True
        )

        await callback.message.answer(
            "⏹ <b>Конкурс завершён досрочно.</b>\n\n"
            "👥 Участников не было.\n"
            "🏆 Победитель не определён.",
            parse_mode="HTML"
        )

        return

    # ID победителя
    winner_id = result

    # Получаем конкурс для текста сообщения
    contest = await get_contest(
        contest_id
    )

    # Уведомляем победителя
    try:

        await callback.bot.send_message(
            winner_id,
            "🎉 <b>ПОЗДРАВЛЯЕМ!</b>\n\n"
            f"Вы выиграли конкурс "
            f"<b>«{contest.title}»</b>! 🏆\n\n"
            f"🎁 Приз: <b>{contest.prize}</b>\n\n"
            "Администратор свяжется с вами "
            "для получения приза.",
            parse_mode="HTML"
        )

    except Exception as e:

        print(
            f"Не удалось отправить сообщение "
            f"победителю {winner_id}: {e}"
        )

    await callback.answer(
        "✅ Конкурс завершён!"
    )

    await callback.message.answer(
        "⏹ <b>Конкурс завершён досрочно!</b>\n\n"
        f"🏆 Победитель:\n"
        f"<code>{winner_id}</code>",
        parse_mode="HTML"
    )