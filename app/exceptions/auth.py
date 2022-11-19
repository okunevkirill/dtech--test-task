__all__ = [
    "CredentialsError",
]

from fastapi import status

from .base import BaseAPIError


class CredentialsError(BaseAPIError):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Incorrect credentials"
