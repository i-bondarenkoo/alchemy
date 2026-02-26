import jwt
from app.core.config import settings
from datetime import datetime, timedelta


def encode_jwt(
    payload: dict,
    key: str = settings.auth_jwt.key,
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode: dict = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    jwt_token: str,
    key: str = settings.auth_jwt.key,
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        jwt=jwt_token,
        key=key,
        algorithms=[algorithm],
    )
    return decoded
