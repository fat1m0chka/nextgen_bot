from sqlalchemy import select

from database.db import async_session
from database.models import User


async def create_request(
    telegram_id,
    username,
    nickname,
    phone
):

    async with async_session() as session:

        user = User(
            telegram_id=telegram_id,
            telegram_username=username,
            nickname=nickname,
            phone=phone,
            status="pending",
            tokens=0
        )

        session.add(user)

        await session.commit()


async def get_pending_requests():

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.status == "pending"
            )
        )

        return result.scalars().all()


async def update_status(
    user_id,
    status
):

    async with async_session() as session:

        user = await session.get(
            User,
            user_id
        )

        user.status = status

        await session.commit()

from database.models import Contest


async def get_contests():

    async with async_session() as session:

        result = await session.execute(
            select(Contest)
        )

        return result.scalars().all()