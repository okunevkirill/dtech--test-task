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
                "signature": "34b4659e3b45b08b6825edefb709ad655c23845c",
                "transaction_id": 1,
                "user_id": 1,
                "bill_id": 1,
                "amount": "100"
            }
        }
