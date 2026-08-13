from aiogram import Router
from aiogram.types import Message
from bot.keyboards.admin import admin_menu
from bot.keyboards.main import main_menu
from bot.utils.admin import is_channel_admin
from config.settings import settings
from database.crud_contest import get_all_contests
from bot.keyboards.client_contest import contest_join
from aiogram.types import CallbackQuery
from database.crud_contest import join_contest
from database.crud_contest import get_finished_contests
from database.crud import get_user


router = Router()


@router.message(lambda message: message.text == "🎮 Привязать аккаунт")
async def link_account(message: Message):
    await message.answer(
        "🎮 Введите ваш ник или номер телефона из клуба:"
    )


@router.message(lambda message: message.text == "🪙 Мои токены")
async def tokens(message: Message):
    await message.answer(
        "🪙 У вас пока 0 токенов."
    )


@router.message(lambda message: message.text == "🏆 Результаты")
async def results(message: Message):
    await message.answer(
        "🏆 Пока розыгрышей не проводилось."
    )


@router.message(lambda m: m.text == "🎁 Активные конкурсы")
async def active_contests(message: Message):

    contests = await get_all_contests()

    if not contests:
        await message.answer(
            "😔 Сейчас активных конкурсов нет."
        )
        return

    for contest in contests:
        await message.answer_photo(
            photo=contest.photo_id,
            caption=(
                f"🏆 {contest.title}\n\n"
                f"📝 {contest.description}\n\n"
                f"🎁 {contest.prize}\n\n"
                f"📅 {contest.start_at}"
        ),
        reply_markup=contest_join(contest.id)
)

@router.callback_query(lambda c: c.data.startswith("join_"))
async def join(callback: CallbackQuery):

    contest_id = int(
        callback.data.split("_")[1]
    )

    ok = await join_contest(
        contest_id,
        callback.from_user.id,
        1
    )

    if ok:

        await callback.answer(
            "Вы участвуете 🎉",
            show_alert=True
        )

    else:

        await callback.answer(
            "Вы уже участвуете",
            show_alert=True
        )

@router.message(lambda m: m.text == "🏆 Победители")
async def winners(message: Message):

    contests = await get_finished_contests()

    if not contests:
        await message.answer(
            "🏆 Пока завершённых конкурсов нет."
        )
        return

    for contest in contests:
        await message.answer_photo(
            contest.photo_id,
            caption=(
                f"🏆 <b>{contest.title}</b>\n\n"
                f"🎁 Приз: {contest.prize}\n"
                f"🥇 Победитель: <b>{contest.winner}</b>"
            ),
            parse_mode="HTML"
        )

@router.message(lambda m: m.text == "👤 Мой профиль")
async def profile(message: Message, bot: Bot):

    user = await get_user(message.from_user.id)

    if not user:
        await message.answer(
            "❌ Вы еще не зарегистрированы."
        )
        return


    statuses = {
        "approved": "✅ Подтвержден",
        "pending": "🟡 На проверке",
        "rejected": "❌ Отклонен"
    }


    photos = await bot.get_user_profile_photos(
        user_id=message.from_user.id,
        limit=1
    )


    text = (
        f"👤 <b>Ваш профиль</b>\n\n"
        f"🆔 ID: <code>{user.telegram_id}</code>\n"
        f"🎮 Ник: {user.nickname or 'Не указан'}\n"
        f"📞 Телефон: {user.phone or 'Не указан'}\n\n"
        f"🪙 Токены: <b>{user.tokens}</b>\n"
        f"📄 Статус: {statuses.get(user.status)}"
    )


    if photos.total_count > 0:

        photo_id = photos.photos[0][-1].file_id

        await message.answer_photo(
            photo=photo_id,
            caption=text,
            parse_mode="HTML"
        )

    else:

        await message.answer(
            text,
            parse_mode="HTML"
        )