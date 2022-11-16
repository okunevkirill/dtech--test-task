__all__ = [
    "router",
]

from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Path, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.database import get_session
from app.exceptions.base import BaseAppException
from app.exceptions.database import ProductNotFoundException
from app.schemas.products import ProductInputSchema, ProductUpdateSchema, ProductOutputSchema

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/",
            response_model=List[ProductOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="List of all products")
async def get_all_products(session: AsyncSession = Depends(get_session)):
    products = await services.database.get_all_products(session)
    return [ProductOutputSchema.from_orm(obj) for obj in products]


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             summary="Add new product")
async def add_product(data: ProductInputSchema,
                      session: AsyncSession = Depends(get_session)):
    product = services.database.add_product(data, session)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product",
        )
    return ProductOutputSchema.from_orm(product)


@router.put("/{product_id}",
            response_model=ProductOutputSchema,
            status_code=status.HTTP_200_OK,
            summary="Update product")
async def update_product(product_id: int,
                         data: ProductUpdateSchema,
                         session: AsyncSession = Depends(get_session)):
    try:
        product = await services.database.update_product(product_id, data, session)
        await session.commit()
        return ProductOutputSchema.from_orm(product)
    except ProductNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )


@router.delete("/{product_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete product")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await services.database.delete_product(product_id, session)
        await session.commit()
        return ""
    except ProductNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )


@router.post("/buy/{product_id}")
async def buy_product(product_id: int = Path(ge=1),
                      bill_id: int = Query(ge=1),
                      user_id: int = Query(ge=1),
                      session: AsyncSession = Depends(get_session)):
    try:
        await services.database.buy_product(product_id, bill_id, user_id, session)
        await session.commit()
        return {"detail": "Purchase completed"}
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
