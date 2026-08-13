from sqlalchemy import select

from database.db import async_session
from database.models import Contest
from database.models import ContestUser
from database.models import ContestUser, User

async def create_contest(
    photo_id,
    title,
    description,
    prize,
    start_at
):

    async with async_session() as session:

        contest = Contest(
            photo_id=photo_id,
            title=title,
            description=description,
            prize=prize,
            start_at=start_at
        )

        session.add(contest)

        await session.commit()


async def get_all_contests():

    async with async_session() as session:

        result = await session.execute(
            select(Contest)
        )

        return result.scalars().all()

async def join_contest(
    contest_id: int,
    telegram_id: int,
    tickets: int
):

    async with async_session() as session:

        user = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        user = user.scalar_one_or_none()


        if not user:
            return False


        if user.tokens < tickets:
            return False


        # списываем токены
        user.tokens -= tickets


        entry = ContestUser(
            contest_id=contest_id,
            telegram_id=telegram_id,
            tickets=tickets
        )


        session.add(entry)

        await session.commit()


        return True

async def get_finished_contests():

    async with async_session() as session:

        result = await session.execute(
            select(Contest).where(
                Contest.winner != None
            )
        )

        return result.scalars().all()