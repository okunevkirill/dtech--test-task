__all__ = [
    "TokenOutputSchema",
    "TokenPayloadSchema",
]

from datetime import datetime
from typing import Union

from pydantic import StrictStr, PositiveInt, StrictBool

from .base import BaseSchema


class TokenOutputSchema(BaseSchema):
    access_token: StrictStr
    refresh_token: StrictStr

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbG...",
                "refresh_token": "eyJhbG..."
            }
        }


class TokenPayloadSchema(BaseSchema):
    exp: Union[datetime, PositiveInt]
    sub: StrictStr
    is_superuser: StrictBool = False
    is_active: StrictBool = False
