__all__ = [
    "router",
]

from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.auth import get_super_user_payload, get_active_user_payload
from app.dependencies.database import get_session
from app.exceptions.base import BaseAppException
from app.schemas.auth import TokenPayloadSchema
from app.schemas.bills import BillOutputSchema, AdminBillOutputSchema

router = APIRouter(prefix="/bills", tags=["Bills"])


@router.get("/",
            response_model=List[AdminBillOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="View all user bills",
            dependencies=[Depends(get_super_user_payload)])
async def get_all_bills(session: AsyncSession = Depends(get_session)):
    bills = await services.database.get_all_bills(session)
    return [AdminBillOutputSchema.from_orm(obj) for obj in bills]


@router.get("/amount/me",
            response_model=List[BillOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="View user balance")
async def get_user_bills(payload: TokenPayloadSchema = Depends(get_active_user_payload),
                         session: AsyncSession = Depends(get_session)):
    try:
        user = await services.database.find_user_by_username(payload.sub, session)
        bills = await services.database.get_user_bills(user, session)
        return [BillOutputSchema.from_orm(obj) for obj in bills]
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
