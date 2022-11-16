__all__ = [
    "BillOutputSchema",
]

from datetime import datetime
from decimal import Decimal

from pydantic import conint

from .base import BaseSchema


class BillOutputSchema(BaseSchema):
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
