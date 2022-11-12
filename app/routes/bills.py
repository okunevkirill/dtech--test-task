__all__ = [
    "router",
]

from fastapi import APIRouter, status

router = APIRouter(prefix="/bills", tags=["Bills"])


@router.get("/",
            status_code=status.HTTP_200_OK,
            summary="View all user bills")
async def get_all_bills():
    return "Place for advertising"


@router.get("/total/me",
            status_code=status.HTTP_200_OK,
            summary="View user balance")
async def get_user_total_bill():
    return "Place for advertising"
