__all__ = [
    "router",
]

from fastapi import APIRouter, status

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/",
            status_code=status.HTTP_200_OK,
            summary="List of all users")
async def get_all_users():
    return "Place for advertising"


@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             summary="New User Registration")
async def register_user():
    return "Place for advertising"


@router.put("/{user_id}",
            status_code=status.HTTP_200_OK,
            summary="Updating user data")
async def update_user(user_id: int):
    return f"Update {user_id} user"


@router.get("/activate/{activate_hexdigest}",
            status_code=status.HTTP_200_OK,
            summary="User activation links")
async def activate_user(activate_hexdigest: str):
    return f"{activate_hexdigest}"
