from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states.contest import ContestState
from bot.keyboards.contest import contest_menu
from database.crud_contest import create_contest
from database.crud_contest import get_all_contests


router = Router()


@router.message(
    lambda m: m.text == "🎁 Конкурсы"
)
async def contest_start(message: Message):

    await message.answer(
        "🎁 Управление конкурсами:",
        reply_markup=contest_menu
    )



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

    data = await state.get_data()

    await create_contest(
        photo_id=data["photo_id"],
        title=data["title"],
        description=data["description"],
        prize=message.text
    )


    await message.answer(
        "✅ Конкурс создан!",
        reply_markup=contest_menu
    )


    await state.clear()

@router.message(lambda m: m.text == "📋 Список конкурсов")
async def contests_list(message: Message):

    contests = await get_all_contests()

    if not contests:
        await message.answer("📭 Конкурсов пока нет.")
        return

    for contest in contests:

        await message.answer_photo(
            photo=contest.photo_id,
            caption=(
                f"🏆 <b>{contest.title}</b>\n\n"
                f"🎁 <b>Приз:</b> {contest.prize}\n\n"
                f"📝 <b>Условия:</b>\n"
                f"{contest.description}"
            )
        )