from aiogram import Bot


async def is_channel_admin(
    bot: Bot,
    channel_id: int,
    user_id: int
):

    admins = await bot.get_chat_administrators(
        channel_id
    )

    for admin in admins:
        if admin.user.id == user_id:
            return True

    return False