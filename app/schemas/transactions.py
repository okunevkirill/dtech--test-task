__all__ = [
    "AdminTransactionOutputSchema",
    "TransactionOutputSchema",
    "TransactionInputSchema",
]

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import conint

from .base import BaseSchema


class TransactionInputSchema(BaseSchema):
    id: Optional[conint(ge=1)] = None
    amount: Decimal
    user_id: conint(ge=1)
    bill_id: conint(ge=1)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "amount": "100.00",
                "user_id": 1,
                "bill_id": 1,
            }
        }


class TransactionOutputSchema(BaseSchema):
    id: conint(ge=1)
    amount: Decimal
    bill_id: conint(ge=1)
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "amount": "42.00",
                "bill_id": 1,
                "created_at": "2022-11-13T15:14:58.657Z"
            }
        }


class AdminTransactionOutputSchema(BaseSchema):
    id: conint(ge=1)
    amount: Decimal
    user_id: conint(ge=1)
    bill_id: conint(ge=1)
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "amount": "100",
                "user_id": 1,
                "bill_id": 1,
                "created_at": "2022-11-13T15:14:58.657Z"
            }
        }
