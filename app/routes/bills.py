__all__ = [
    "router",
]

from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.database import get_session
from app.exceptions.base import BaseAppException
from app.schemas.bills import BillOutputSchema

router = APIRouter(prefix="/bills", tags=["Bills"])


@router.get("/",
            response_model=List[BillOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="View all user bills")
async def get_all_bills(session: AsyncSession = Depends(get_session)):
    bills = await services.database.get_all_bills(session)
    return [BillOutputSchema.from_orm(obj) for obj in bills]


@router.get("/amount/me",
            status_code=status.HTTP_200_OK,
            summary="View user balance")
async def get_user_bills(user_id: int = Query(ge=1),
                         session: AsyncSession = Depends(get_session)):
    try:
        bills = await services.database.get_user_bills(user_id, session)
        return [BillOutputSchema.from_orm(obj) for obj in bills]
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
