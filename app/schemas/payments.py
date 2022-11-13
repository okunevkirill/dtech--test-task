__all__ = [
    "WebhookInputSchema",
]

from decimal import Decimal

from pydantic import StrictStr, conint

from .base import BaseSchema


class WebhookInputSchema(BaseSchema):
    signature: StrictStr
    transaction_id: conint(ge=1)
    user_id: conint(ge=1)
    bill_id: conint(ge=1)
    amount: Decimal

    class Config:
        schema_extra = {
            "example": {
                "signature": "f4eae5b2881d8b6a1455f62502d08b2258d80084",
                "transaction_id": 1,
                "user_id": 1,
                "bill_id": 1,
                "amount": "100"
            }
        }
