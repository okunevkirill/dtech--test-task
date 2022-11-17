__all__ = [
    "get_activate_hexdigest",
    "get_hashed_password",
    "verify_password",
]

import hashlib
import os

from passlib.context import CryptContext
from passlib.handlers.digests import hex_sha1

from app.schemas.payments import WebhookInputSchema
from app.settings import SETTINGS

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    salt = SETTINGS.APP_SECRET_KEY.get_secret_value()
    password += salt
    return PASSWORD_CONTEXT.hash(password)


def verify_password(password: str, compared_hash: str) -> bool:
    salt = SETTINGS.APP_SECRET_KEY.get_secret_value()
    password += salt
    return PASSWORD_CONTEXT.verify(password, compared_hash)


def get_activate_hexdigest(username: str) -> str:
    encoding = SETTINGS.__config__.env_file_encoding
    salt = os.urandom(32)
    return hashlib.sha256(username.encode(encoding) + salt).hexdigest()


def verify_webhook(data: WebhookInputSchema) -> bool:
    signature = hex_sha1.hash(
        f"{SETTINGS.WEBHOOK_KEY.get_secret_value()}:"
        f"{data.transaction_id}:"
        f"{data.user_id}:"
        f"{data.bill_id}:"
        f"{data.amount}"
    )
    return signature == data.signature
