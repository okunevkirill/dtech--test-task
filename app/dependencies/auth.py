__all__ = [
    "get_jwt_token",
    "get_jwt_payload",
    "get_active_user_payload",
    "get_super_user_payload",
]

from fastapi import Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic.error_wrappers import ValidationError
from jose import jwt, JWTError

from app.settings import SETTINGS
from app.exceptions.auth import CredentialsError
from app.schemas.auth import TokenPayloadSchema

jwt_security = HTTPBearer()


async def get_jwt_token(
        credentials: HTTPAuthorizationCredentials = Security(jwt_security)
) -> str:
    return credentials.credentials


async def get_jwt_payload(
        credentials: HTTPAuthorizationCredentials = Security(jwt_security)
) -> TokenPayloadSchema:
    token = credentials.credentials
    try:
        data = jwt.decode(
            token, SETTINGS.JWT_SECRET_KEY.get_secret_value(), algorithms=[SETTINGS.JWT_ALGORITHM])
        return TokenPayloadSchema(**data)
    except (JWTError, ValidationError):
        raise CredentialsError(message="Invalid token")


async def get_active_user_payload(
        payload: TokenPayloadSchema = Depends(get_jwt_payload)
) -> TokenPayloadSchema:
    if not payload.is_active:
        raise CredentialsError(message="User not activated")
    return payload


async def get_super_user_payload(
        payload: TokenPayloadSchema = Depends(get_active_user_payload)
) -> TokenPayloadSchema:
    if not payload.is_superuser:
        raise CredentialsError(message="Not enough rights")
    return payload
