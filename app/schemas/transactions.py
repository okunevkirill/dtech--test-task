__all__ = [
    "TransactionOutputSchema",
]

from datetime import datetime
from decimal import Decimal

from pydantic import conint

from .base import BaseSchema


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
