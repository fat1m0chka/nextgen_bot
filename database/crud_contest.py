from sqlalchemy import select

from database.db import async_session
from database.models import Contest


async def create_contest(photo_id, title, description, prize):

    async with async_session() as session:

        contest = Contest(
            photo_id=photo_id,
            title=title,
            description=description,
            prize=prize
        )

        session.add(contest)
        await session.commit()


async def get_all_contests():

    async with async_session() as session:

        result = await session.execute(
            select(Contest)
        )

        return result.scalars().all()