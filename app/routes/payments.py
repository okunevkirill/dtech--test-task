__all__ = [
    "router",
]

from fastapi import APIRouter, status

router = APIRouter(prefix="/payment", tags=["Payments"])


@router.post("/webhook",
             status_code=status.HTTP_200_OK,
             summary="Request for money transfer")
async def transfer_funds():
    return "Place for advertising"
