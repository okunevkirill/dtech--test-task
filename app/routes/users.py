__all__ = [
    "router",
]

from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.dependencies.auth import get_super_user_payload
from app.dependencies.database import get_session
from app.exceptions.database import UserNotFoundException
from app.schemas.users import AdminUserOutputSchema, UserInputSchema, UserUpdateSchema
from app.settings import SETTINGS

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/",
            response_model=List[AdminUserOutputSchema],
            status_code=status.HTTP_200_OK,
            summary="List of all users",
            dependencies=[Depends(get_super_user_payload)])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await services.database.get_all_users(session)
    return [AdminUserOutputSchema.from_orm(obj) for obj in users]


@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             summary="New User Registration")
async def register_user(
        data: UserInputSchema,
        session: AsyncSession = Depends(get_session),
):
    user = services.database.add_user(data, session)
    try:
        await session.commit()
        return (
            f"{SETTINGS.APP_PROTOCOL}://"
            f"{SETTINGS.APP_HOST}:"
            f"{SETTINGS.APP_PORT}/users/activate/{user.activate_hexdigest}"
        )
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists",
        )


@router.put("/{user_id}",
            status_code=status.HTTP_200_OK,
            summary="Updating user data",
            dependencies=[Depends(get_super_user_payload)])
async def update_user(user_id: int,
                      data: UserUpdateSchema,
                      session: AsyncSession = Depends(get_session)):
    try:
        user = await services.database.update_user(user_id, data, session)
        await session.commit()
        return AdminUserOutputSchema.from_orm(user)
    except UserNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=err.message,
        )
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A user with this 'username' already exists",
        )


@router.get("/activate/{activate_hexdigest}",
            status_code=status.HTTP_200_OK,
            summary="User activation links")
async def activate_user(activate_hexdigest: str,
                        session: AsyncSession = Depends(get_session)):
    try:
        await services.database.activate_user(activate_hexdigest, session)
        await session.commit()
        return {"detail": "User has been activated"}
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Activation link is not correct"
        )
