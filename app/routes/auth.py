__all__ = [
    "router",
]

from fastapi import APIRouter, status

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login",
             status_code=status.HTTP_200_OK,
             summary="Getting tokens to interact with the application")
async def login():
    return "Place for advertising"


@router.get("/logout",
            status_code=status.HTTP_200_OK,
            summary="Removing a token refresh token")
async def logout():
    return "Place for advertising"


@router.get("/refresh-token",
            status_code=status.HTTP_200_OK,
            summary="Application access token refresh")
async def refresh_token():
    return "Place for advertising"
