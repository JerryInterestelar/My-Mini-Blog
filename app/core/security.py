from typing import Any
import jwt
from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone


from app.core.config import settings

password_hash = PasswordHash.recommended()


def get_password_hash(raw_password: str) -> str:
    return password_hash.hash(raw_password)


def verify_password_hash(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(
    data: dict[str, Any], expires_at: timedelta | None = None
) -> str:
    data_to_encode = data.copy()

    expire_date: datetime

    if expires_at:
        expire_date = datetime.now(timezone.utc) + expires_at
    else:
        expire_date = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    data_to_encode.update({'exp': expire_date})
    encoded_jwt = jwt.encode(data_to_encode, settings.SECRET_KEY, settings.ALGORITHM)  # type: ignore

    return encoded_jwt
