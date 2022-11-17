__all__ = [
    "router",
]

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.database import get_session
from app.exceptions.base import BaseAppException
from app.schemas.payments import WebhookInputSchema

router = APIRouter(prefix="/payment", tags=["Payments"])


@router.post("/webhook",
             status_code=status.HTTP_200_OK,
             summary="Request for money transfer")
async def transfer_funds(data: WebhookInputSchema,
                         session: AsyncSession = Depends(get_session)):
    if not services.utils.verify_webhook(data):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect signature",
        )
    try:
        await services.database.transfer_funds(data, session)
        await session.commit()
        return {"detail": "Funds credited"}
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
