from aiogram import Router
from aiogram.types import CallbackQuery

from config.settings import settings
from bot.utils.check_subscription import check_subscription
from bot.keyboards.main import main_menu
from database.crud import get_user, create_user  # или твоя функция регистрации из crud.py


router = Router()


@router.callback_query(lambda c: c.data == "check_sub")
async def check(callback: CallbackQuery):

    result = await check_subscription(
        callback.bot,
        callback.from_user.id,
        settings.CHANNEL_ID
    )

    if result:
        # 1. Проверяем/создаем запись пользователя в БД при первом входе
        user = await get_user(callback.from_user.id)
        if not user:
            await create_user(
                telegram_id=callback.from_user.id,
                telegram_username=callback.from_user.username
            )

        # 2. Гасим спиннер на инлайн-кнопке
        await callback.answer("Подписка подтверждена! 🎉")

        # 3. Редактируем сообщение с проверкой
        await callback.message.edit_text(
            "✅ Подписка подтверждена!"
        )

        # 4. Отправляем приветствие и выкатываем Reply-клавиатуру главного меню
        # (если main_menu это функция, пиши main_menu(), если готовая переменная — main_menu)
        menu_kb = main_menu() if callable(main_menu) else main_menu
        await callback.message.answer(
            "Добро пожаловать в клуб! Выберите действие:",
            reply_markup=menu_kb
        )

    else:
        await callback.answer(
            "❌ Вы еще не подписались на канал!",
            show_alert=True
        )
