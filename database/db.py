from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)


DATABASE_URL = "sqlite+aiosqlite:///database/lottery.db"


engine = create_async_engine(
    DATABASE_URL,
    echo=True
)


async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        yield session


async def init_db():
    from database.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)