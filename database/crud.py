from sqlalchemy import select

from database.db import async_session
from database.models import User
from sqlalchemy import func


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

async def get_user(telegram_id):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        return result.scalar_one_or_none()


async def get_user_by_phone(phone):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.phone == phone
            )
        )

        return result.scalar_one_or_none()

async def add_tokens(user_id: int, tokens: int):
    async with async_session() as session:

        user = await session.get(User, user_id)

        if not user:
            return None

        user.tokens += tokens

        await session.commit()

        return user

from sqlalchemy import select

async def get_users():

    async with async_session() as session:

        result = await session.execute(
            select(User)
        )

        return result.scalars().all()

async def get_statistics():

    async with async_session() as session:

        total = await session.scalar(
            select(func.count(User.id))
        )

        approved = await session.scalar(
            select(func.count(User.id))
            .where(User.status == "approved")
        )

        pending = await session.scalar(
            select(func.count(User.id))
            .where(User.status == "pending")
        )

        rejected = await session.scalar(
            select(func.count(User.id))
            .where(User.status == "rejected")
        )

        tokens = await session.scalar(
            select(func.sum(User.tokens))
        )

        return {
            "total": total or 0,
            "approved": approved or 0,
            "pending": pending or 0,
            "rejected": rejected or 0,
            "tokens": tokens or 0,
        }

async def get_user(telegram_id):

    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        return result.scalar_one_or_none()

async def get_finished_contests():

    async with async_session() as session:

        result = await session.execute(
            select(Contest).where(
                Contest.winner.is_not(None)
            )
        )

        return result.scalars().all()

async def get_user_by_id(user_id):

    async with async_session() as session:

        user = await session.get(
            User,
            user_id
        )

        return user

async def can_join_contest(
    telegram_id: int
):
    async with async_session() as session:

        result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            return False, "not_registered"

        if user.status != "approved":
            return False, "not_approved"

        if user.tokens <= 0:
            return False, "no_tokens"

        return True, user