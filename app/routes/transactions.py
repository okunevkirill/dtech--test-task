__all__ = [
    "router",
]

from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.auth import get_super_user_payload, get_active_user_payload
from app.dependencies.database import get_session
from app.exceptions.base import BaseAppException
from app.schemas.auth import TokenPayloadSchema
from app.schemas.transactions import AdminTransactionOutputSchema, TransactionOutputSchema

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/",
            response_model=List[AdminTransactionOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="Request a list of transactions",
            dependencies=[Depends(get_super_user_payload)])
async def get_all_transactions(session: AsyncSession = Depends(get_session)):
    transactions = await services.database.get_all_transactions(session)
    return [AdminTransactionOutputSchema.from_orm(obj) for obj in transactions]


@router.get("/me",
            response_model=List[TransactionOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="User transactions")
async def get_user_transactions(payload: TokenPayloadSchema = Depends(get_active_user_payload),
                                session: AsyncSession = Depends(get_session)):
    try:
        user = await services.database.find_user_by_username(payload.sub, session)
        transactions = await services.database.get_user_transactions(user, session)
        return [TransactionOutputSchema.from_orm(obj) for obj in transactions]
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
