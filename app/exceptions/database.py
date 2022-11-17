__all__ = [
    "BillNotFoundException",
    "InsufficientFundsException",
    "ProductNotFoundException",
    "TransactionNotFoundException",
    "UserNotFoundException",
]

from .base import BaseAppException


class UserNotFoundException(BaseAppException):
    message = "User not found"


class ProductNotFoundException(BaseAppException):
    message = "Product not found"


class BillNotFoundException(BaseAppException):
    message = "Bill not found"


class InsufficientFundsException(BaseAppException):
    message = "There are not enough funds on the specified account"


class TransactionNotFoundException(BaseAppException):
    message = "Transaction not found"
