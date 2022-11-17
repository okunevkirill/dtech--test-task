__all__ = [
    "UserInputSchema",
    "UserUpdateSchema",
    "AdminUserOutputSchema",
]

from datetime import datetime

from typing import Optional

from pydantic import StrictStr, Field, StrictBool, conint

from .base import BaseSchema, UsernameField


class UserInputSchema(BaseSchema):
    username: UsernameField
    password: StrictStr = Field(min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "username": "kirill",
                "password": "password"
            }
        }


class UserUpdateSchema(BaseSchema):
    username: Optional[UsernameField] = None
    is_superuser: Optional[StrictBool] = None
    is_active: Optional[StrictBool] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "kirill",
                "is_superuser": False,
                "is_active": True
            }
        }


class AdminUserOutputSchema(BaseSchema):
    id: conint(ge=1)
    username: UsernameField
    is_superuser: StrictBool
    is_active: StrictBool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "kirill",
                "is_superuser": True,
                "is_active": True,
                "created_at": "2022-11-13T15:14:58.657Z",
                "updated_at": "2022-11-13T15:14:58.657Z"
            }
        }
