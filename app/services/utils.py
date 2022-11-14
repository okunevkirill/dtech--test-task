__all__ = [
    "get_hashed_password",
    "verify_password",
]

from passlib.context import CryptContext

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
