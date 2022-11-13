__all__ = [
    "ProductInputSchema",
    "ProductUpdateSchema",
    "ProductOutputSchema",
]

from decimal import Decimal
from typing import Optional

from pydantic import StrictStr, conint

from .base import BaseSchema


class ProductInputSchema(BaseSchema):
    name: StrictStr
    description: StrictStr
    price: Decimal

    class Config:
        schema_extra = {
            "example": {
                "name": "Product 001",
                "description": "Mega description 001",
                "price": 42.42
            }
        }


class ProductUpdateSchema(BaseSchema):
    name: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    price: Optional[Decimal] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Product 001",
                "description": "Mega description 001",
                "price": "42.42"
            }
        }


class ProductOutputSchema(BaseSchema):
    id: conint(ge=1)
    name: StrictStr
    description: StrictStr
    price: Decimal

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Product 001",
                "description": "Mega description 001",
                "price": "42.42"
            }
        }
