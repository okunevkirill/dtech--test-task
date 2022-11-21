__all__ = [
    "BillInputSchema",
    "BillOutputSchema",
    "AdminBillOutputSchema",
]

from datetime import datetime
from decimal import Decimal

from pydantic import conint

from .base import BaseSchema


class BillInputSchema(BaseSchema):
    user_id: conint(ge=1)
    amount: Decimal = 0

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": 1,
                "amount": "100"
            }
        }


class BillOutputSchema(BaseSchema):
    id: conint(ge=1)
    amount: Decimal
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "amount": "300",
                "created_at": "2022-11-13T15:14:58.657Z"
            }
        }


class AdminBillOutputSchema(BaseSchema):
    id: conint(ge=1)
    amount: Decimal
    user_id: conint(ge=1)
    created_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "amount": "300",
                "user_id": 1,
                "created_at": "2022-11-13T15:14:58.657Z"
            }
        }
