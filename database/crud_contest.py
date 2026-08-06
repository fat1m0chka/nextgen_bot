from sqlalchemy import select

from database.db import async_session
from database.models import Contest
from database.models import ContestUser


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

async def join_contest(contest_id, telegram_id):

    async with async_session() as session:

        result = await session.execute(
            select(ContestUser).where(
                ContestUser.contest_id == contest_id,
                ContestUser.telegram_id == telegram_id
            )
        )

        if result.scalar():
            return False

        session.add(
            ContestUser(
                contest_id=contest_id,
                telegram_id=telegram_id
            )
        )

        await session.commit()

        return True