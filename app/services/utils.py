__all__ = [
    "get_activate_hexdigest",
    "get_hashed_password",
    "verify_password",
    "verify_webhook",
]

import hashlib
import os
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from passlib.handlers.digests import hex_sha1

from app.db import models
from app.schemas.auth import TokenPayloadSchema
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


# -----------------------------------------------------------------------------
def create_token(subject: models.User, expires_delta: int) -> str:
    current_time = datetime.utcnow()
    expires_delta = current_time + timedelta(minutes=expires_delta)
    to_encode = TokenPayloadSchema(
        exp=expires_delta,
        sub=subject.username,
        is_superuser=subject.is_superuser,
        is_active=subject.is_active
    )
    encoded_jwt = jwt.encode(
        to_encode.dict(),
        SETTINGS.JWT_SECRET_KEY.get_secret_value(),
        algorithm=SETTINGS.JWT_ALGORITHM
    )
    return encoded_jwt
