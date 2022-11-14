__all__ = [
    "BaseAppException",
    "BaseAPIError",
]

from typing import Optional

from fastapi import HTTPException, status


class BaseAppException(Exception):
    message: str = "Unexpected application exception"

    def __init__(self, message: Optional[str] = None):
        if message is not None:
            self.message = message

    def __str__(self):
        return f"{self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.message}')"


class BaseAPIError(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Unexpected API error"

    def __init__(self, status_code: Optional[int] = None, message: Optional[str] = None):
        if status_code is None:
            status_code = self.status_code
        if message is None:
            message = self.message
        super().__init__(status_code, detail=message)
