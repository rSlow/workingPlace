import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

Base = declarative_base()
engine = create_async_engine(
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@postgres/{POSTGRES_DB}",
)
Session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
# jdbc:postgresql://192.168.112.2:5432/workedPlace

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
