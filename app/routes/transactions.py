__all__ = [
    "router",
]

from typing import List

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.database import get_session
from app.exceptions.base import BaseAppException
from app.schemas.transactions import AdminTransactionOutputSchema, TransactionOutputSchema

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/",
            response_model=List[AdminTransactionOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="Request a list of transactions")
async def get_all_transactions(session: AsyncSession = Depends(get_session)):
    transactions = await services.database.get_all_transactions(session)
    return [AdminTransactionOutputSchema.from_orm(obj) for obj in transactions]


@router.get("/me",
            response_model=List[TransactionOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="User transactions")
async def get_user_transactions(user_id: int = Query(ge=1),
                                session: AsyncSession = Depends(get_session)):
    try:
        transactions = await services.database.get_user_transactions(user_id, session)
        return [TransactionOutputSchema.from_orm(obj) for obj in transactions]
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
