__all__ = [

]

from pydantic import StrictStr, PositiveInt, StrictBool, conint

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


class TokenAccessPayloadSchema(BaseSchema):
    exp: PositiveInt
    iat: PositiveInt
    sub: conint(ge=1)
    scope: StrictStr
    is_superuser: StrictBool = False
    is_active: StrictBool = False


class TokenRefreshPayloadSchema(BaseSchema):
    exp: PositiveInt
    iat: PositiveInt
    sub: conint(ge=1)
    scope: StrictStr
