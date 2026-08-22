from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Integer
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True
    )

    telegram_username: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    nickname: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    tokens: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String,
        default="pending"
    )

class Contest(Base):
    __tablename__ = "contests"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    photo_id: Mapped[str] = mapped_column(
        String
    )

    title: Mapped[str] = mapped_column(
        String
    )

    description: Mapped[str] = mapped_column(
        String
    )

    prize: Mapped[str] = mapped_column(
        String
    )

    start_at: Mapped[str] = mapped_column(
        String
    )

    end_at: Mapped[str] = mapped_column(
        String
    )

    winner_count: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    status: Mapped[str] = mapped_column(
        String,
        default="active"
    )

class ContestUser(Base):
    __tablename__ = "contest_users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    contest_id: Mapped[int] = mapped_column(
        ForeignKey("contests.id")
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger
    )