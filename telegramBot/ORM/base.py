import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

Base = declarative_base()
engine = create_async_engine(os.getenv("DB_URI"), echo=True)
Session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    try:
        import asyncio

        asyncio.run(init_database())
    except ImportError:
        raise
