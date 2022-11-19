__all__ = [
    "router",
]

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.auth import get_active_user_payload, get_jwt_token
from app.dependencies.database import get_session
from app.exceptions.auth import CredentialsError
from app.exceptions.base import BaseAppException
from app.schemas.auth import TokenOutputSchema, TokenPayloadSchema
from app.schemas.users import UserInputSchema
from app.settings import SETTINGS

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login",
             status_code=status.HTTP_200_OK,
             summary="Getting tokens to interact with the application")
async def login(data: UserInputSchema,
                session: AsyncSession = Depends(get_session)):
    try:
        user = await services.database.find_user_by_username(data.username, session)
        if not services.utils.verify_password(data.password, user.password):
            raise CredentialsError
        atoken = services.utils.create_token(user, SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
        rtoken = services.utils.create_token(user, SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES)
        user.rtoken = rtoken
        await session.commit()
        return TokenOutputSchema(access_token=atoken, refresh_token=rtoken)
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )


@router.get("/logout",
            status_code=status.HTTP_200_OK,
            summary="Removing a token refresh token")
async def logout(payload: TokenPayloadSchema = Depends(get_active_user_payload),
                 session: AsyncSession = Depends(get_session)):
    try:
        user = await services.database.find_user_by_username(payload.sub, session)
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
    user.rtoken = None
    await session.commit()
    return {"detail": "Refresh token has been removed"}


@router.get("/refresh-token",
            status_code=status.HTTP_200_OK,
            summary="Application access token refresh")
async def refresh_token(token: str = Depends(get_jwt_token),
                        payload: TokenPayloadSchema = Depends(get_active_user_payload),
                        session: AsyncSession = Depends(get_session)):
    try:
        user = await services.database.find_user_by_username(payload.sub, session)
    except BaseAppException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
    if user.rtoken != token:
        raise CredentialsError
    atoken = services.utils.create_token(user, SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": atoken}
