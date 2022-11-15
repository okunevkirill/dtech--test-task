__all__ = [
    "get_all_users",
]

from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app import schemas
from app.exceptions.base import BaseAppException
from app.services.utils import get_hashed_password, get_activate_hexdigest
from app.exceptions.database import UserNotFoundException


async def find_user_by_id(user_id: int, session: AsyncSession) -> models.User:
    user = await session.get(models.User, user_id)
    if user is None:
        raise UserNotFoundException
    return user


async def get_all_users(session: AsyncSession) -> List[models.User]:
    result = await session.execute(select(models.User))
    return result.scalars().all()


def add_user(data: schemas.users.UserInputSchema, session: AsyncSession) -> models.User:
    data.password = get_hashed_password(data.password)
    user = models.User(**data.dict())
    user.activate_hexdigest = get_activate_hexdigest(user.username)
    session.add(user)
    return user


async def update_user(user_id: int,
                      data: schemas.users.UserUpdateSchema,
                      session: AsyncSession) -> models.User:
    user = await find_user_by_id(user_id, session)

    for key, value in data:
        if value is None:
            continue
        setattr(user, key, value)

    if any(data.dict().values()):
        user.updated_at = datetime.utcnow()
    return user


async def activate_user(activate_hexdigest: str, session: AsyncSession):
    result = await session.execute(
        select(models.User).where(
            models.User.activate_hexdigest == activate_hexdigest)
    )
    try:
        user = result.scalars().one()
    except NoResultFound:
        raise UserNotFoundException
    user.is_active = True
    user.activate_hexdigest = None


async def create_superuser(username: str, password: str, async_generator):
    session = await async_generator.asend(None)
    password = get_hashed_password(password)
    user = models.User(username=username,
                       password=password,
                       is_superuser=True,
                       is_active=True)
    session.add(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise BaseAppException
