from sqlalchemy import select

from database.db import async_session
from database.models import Contest, ContestUser, User
import random

# =========================
# СОЗДАНИЕ КОНКУРСА
# =========================

async def create_contest(
    photo_id,
    title,
    description,
    prize,
    start_at,
    end_at
):
    async with async_session() as session:

        contest = Contest(
            photo_id=photo_id,
            title=title,
            description=description,
            prize=prize,
            start_at=start_at,
            end_at=end_at,
            winner_count=1,
            status="active"
        )

        session.add(contest)

        await session.commit()


# =========================
# ВСЕ КОНКУРСЫ
# =========================

async def get_all_contests():
    async with async_session() as session:

        result = await session.execute(
            select(Contest)
        )

        return result.scalars().all()


# =========================
# ПОЛУЧИТЬ КОНКУРС
# =========================

async def get_contest(contest_id: int):
    async with async_session() as session:

        result = await session.execute(
            select(Contest).where(
                Contest.id == contest_id
            )
        )

        return result.scalar_one_or_none()


# =========================
# УЧАСТИЕ В КОНКУРСЕ
# =========================

async def join_contest(
    contest_id: int,
    telegram_id: int
):
    async with async_session() as session:

        # Проверяем пользователя
        result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            return "not_registered"

        # Только одобренные пользователи
        if user.status != "approved":
            return "not_approved"

        # Нужен хотя бы 1 токен
        if user.tokens <= 0:
            return "no_tokens"

        # Проверяем, участвует ли уже
        result = await session.execute(
            select(ContestUser).where(
                ContestUser.contest_id == contest_id,
                ContestUser.telegram_id == telegram_id
            )
        )

        participant = result.scalar_one_or_none()

        if participant:
            return "already_joined"

        # Добавляем участника
        participant = ContestUser(
            contest_id=contest_id,
            telegram_id=telegram_id
        )

        session.add(participant)

        await session.commit()

        return "joined"


# =========================
# ПРОВЕРКА УЧАСТИЯ
# =========================

async def is_joined(
    contest_id: int,
    telegram_id: int
):
    async with async_session() as session:

        result = await session.execute(
            select(ContestUser).where(
                ContestUser.contest_id == contest_id,
                ContestUser.telegram_id == telegram_id
            )
        )

        participant = result.scalar_one_or_none()

        return participant is not None


# =========================
# УЧАСТНИКИ КОНКУРСА
# =========================

async def get_contest_participants(
    contest_id: int
):
    async with async_session() as session:

        result = await session.execute(
            select(ContestUser).where(
                ContestUser.contest_id == contest_id
            )
        )

        return result.scalars().all()

# =========================
# ЗАВЕРШЕННЫЕ КОНКУРСЫ
# =========================

async def get_finished_contests():
    async with async_session() as session:

        result = await session.execute(
            select(Contest).where(
                Contest.winner.is_not(None)
            )
        )

        return result.scalars().all()

# =========================
# ДОСРОЧНОЕ ЗАВЕРШЕНИЕ КОНКУРСА
# =========================

async def finish_contest(contest_id: int):
    async with async_session() as session:

        # Получаем конкурс
        result = await session.execute(
            select(Contest).where(
                Contest.id == contest_id
            )
        )

        contest = result.scalar_one_or_none()

        if not contest:
            return "not_found"

        if contest.status == "finished":
            return "already_finished"

        # Получаем участников
        result = await session.execute(
            select(ContestUser).where(
                ContestUser.contest_id == contest_id
            )
        )

        participants = result.scalars().all()

        if not participants:
            contest.status = "finished"
            contest.winner = None

            await session.commit()

            return "no_participants"

        # Пока один победитель
        winner = random.choice(participants)

        contest.winner = winner.telegram_id
        contest.status = "finished"

        await session.commit()

        return winner.telegram_id