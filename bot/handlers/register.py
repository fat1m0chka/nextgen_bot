from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import re
from bot.states.register import RegisterState
from database.crud import create_request, get_user

router = Router()


@router.message(lambda message: message.text == "🎮 Привязать аккаунт")
async def start_register(
    message: Message,
    state: FSMContext
):
    await state.set_state(RegisterState.nickname)

    await message.answer(
        "🎮 Введите ваш ник в клубе:"
    )


@router.message(RegisterState.nickname)
async def get_nickname(
    message: Message,
    state: FSMContext
):
    nickname = (message.text or "").strip()

    if not re.fullmatch(r"[А-Яа-яA-Za-z0-9_-]{2,32}", nickname):
        await message.answer(
            "❌ Некорректный ник.\n\n"
            "Разрешены:\n"
            "• русские и английские буквы\n"
            "• цифры\n"
            "• символы _ и -\n\n"
            "Длина: от 2 до 32 символов."
        )
        return

    await state.update_data(
        nickname=nickname
    )

    await state.set_state(RegisterState.phone)

    await message.answer(
        "📱 Теперь введите номер телефона:\n"
        "Введите номер без +7, 7 и 8"
    )


@router.message(RegisterState.phone)
async def get_phone(
    message: Message,
    state: FSMContext
):
    user = await get_user(message.from_user.id)

    if user:

        if user.status == "approved":
            await message.answer(
                "✅ Ваш аккаунт уже подтвержден."
            )

        elif user.status == "pending":
            await message.answer(
                "⏳ Ваша заявка уже находится на проверке."
            )

        else:
            await message.answer(
                "❌ Ваша заявка была отклонена."
            )

        await state.clear()
        return




    phone = message.text.strip()

    if not re.fullmatch(r"\d{10}", phone):
        await message.answer(
            "❌ Введите номер без +7 и 7\n\n"
            "Пример:\n"
            "9991234567"
        )
        return


    data = await state.get_data()


    await create_request(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        nickname=data["nickname"],
        phone=phone
    )


    await message.answer(
        f"✅ Заявка создана!\n\n"
        f"🎮 Ник: {data['nickname']}\n"
        f"📱 Телефон: {phone}\n\n"
        f"Ожидайте проверки администратора."
    )


    await state.clear()