__all__ = [
    "router",
]

from fastapi import APIRouter, status

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/",
            status_code=status.HTTP_200_OK,
            summary="Request a list of transactions")
async def get_all_transactions():
    return "Place for advertising"


@router.get("/me",
            status_code=status.HTTP_200_OK,
            summary="User transactions")
async def get_user_transactions():
    return "Place for advertising"
