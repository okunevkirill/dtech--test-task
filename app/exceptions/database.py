__all__ = [
    "UserNotFoundException",
]

from .base import BaseAppException


class UserNotFoundException(BaseAppException):
    message = "User not found"
