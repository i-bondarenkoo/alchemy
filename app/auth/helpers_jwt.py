from app.core.config import settings
from datetime import timedelta
from app.auth.jwt import encode_jwt, decode_jwt
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    data: dict = {
        "type": token_type,
    }
    data.update(token_data)
    return encode_jwt(
        payload=data,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(
    user: User,
):
    token_data = {
        "username": user.username,
        "email": user.email,
        "id": user.id,
    }
    return create_jwt(
        token_type="access",
        token_data=token_data,
    )


def create_refresh_token(
    user: User,
):
    token_data = {
        "sub": user.username,
    }
    return create_jwt(
        token_type="refresh",
        token_data=token_data,
        expire_timedelta=timedelta(
            days=settings.auth_jwt.refrest_token_expire_days,
        ),
    )


def validate_token_type(
    token: str,
) -> bool:
    current_token_type = decode_jwt(token)
    if current_token_type == "access":
        return "access"
    return "refresh"
