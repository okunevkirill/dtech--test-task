from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import async_session

__all__ = [
    "get_session",
]


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
