__all__ = [
    "async_session",
    "Base",
    "engine",
    "init_models",
]

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import SETTINGS

DATABASE_URL = (
    "postgresql+asyncpg:"
    f"//{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD.get_secret_value()}"
    f"@{SETTINGS.POSTGRES_HOST}:{SETTINGS.POSTGRES_PORT}/{SETTINGS.POSTGRES_DATABASE_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=False)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
