__all__ = [
    "get_all_users",
]

from datetime import datetime
from typing import List, Any, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models
from app import schemas
from app.exceptions.base import BaseAppException
from app.schemas.base import BaseSchema
from app.services.utils import get_hashed_password, get_activate_hexdigest
from app.exceptions.database import (
    UserNotFoundException, ProductNotFoundException,
    BillNotFoundException, InsufficientFundsException,
)


def setter_from_schema(obj: Any,
                       data: BaseSchema,
                       date_field_name: str = "updated_at"):
    for key, value in data:
        if value is None:
            continue
        setattr(obj, key, value)
    if any(data.dict().values()):
        setattr(obj, date_field_name, datetime.utcnow())


# -----------------------------------------------------------------------------
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
    setter_from_schema(user, data)
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


# -----------------------------------------------------------------------------
async def find_product_by_id(product_id: int, session: AsyncSession) -> models.Product:
    product = await session.get(models.Product, product_id)
    if product is None:
        raise ProductNotFoundException
    return product


async def get_all_products(session: AsyncSession) -> List[models.Product]:
    result = await session.execute(
        select(models.Product).order_by(models.Product.name))
    return result.scalars().all()


def add_product(data: schemas.products.ProductInputSchema, session: AsyncSession):
    product = models.Product(**data.dict())
    session.add(product)
    return product


async def update_product(product_id: int,
                         data: schemas.products.ProductUpdateSchema,
                         session: AsyncSession) -> models.Product:
    product = await find_product_by_id(product_id, session)
    setter_from_schema(product, data)
    return product


async def delete_product(product_id: int, session: AsyncSession):
    product = await find_product_by_id(product_id, session)
    await session.delete(product)


async def buy_product(product_id: int,
                      bill_id: int,
                      user_id: int,
                      session: AsyncSession):
    product = await find_product_by_id(product_id, session)
    user = await find_user_by_id(user_id, session)
    # [!] Because session asynchronous run it in a sync context
    user_bills = await session.run_sync(lambda _: user.bills)
    bill: Optional[models.Bill] = None
    for item in user_bills:
        if item.id == bill_id:
            bill = item
            break
    if bill is None:
        raise BillNotFoundException
    if bill.amount < product.price:
        raise InsufficientFundsException
    bill.amount -= product.price


# -----------------------------------------------------------------------------
async def get_all_transactions(session: AsyncSession) -> List[models.Transaction]:
    result = await session.execute(select(models.Transaction))
    return result.scalars().all()


async def get_user_transactions(user_id: int, session: AsyncSession) -> List[models.Transaction]:
    user = await find_user_by_id(user_id, session)
    result = await session.run_sync(lambda _: user.transactions)
    return result
