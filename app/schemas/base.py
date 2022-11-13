__all__ = [
    "BaseSchema",
    "UsernameField",
]

import re

from pydantic import BaseModel, StrictStr

_USERNAME_REGEX = re.compile(r"^[a-zA-z][a-zA-Z0-9]{2,}$")


class BaseSchema(BaseModel):
    pass


class UsernameField(StrictStr):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern="^[a-zA-z][a-zA-Z0-9]{2,}$",
            examples=["username", "A123456"],
        )

    @classmethod
    def validate(cls, value):
        match = _USERNAME_REGEX.fullmatch(value)
        if not match:
            raise ValueError("Invalid username format")
        # [!] The class is returned specifically for correct annotation
        return cls(f'{match.group()}')
