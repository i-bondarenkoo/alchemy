from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.schemas.user import UserLoginSchema
from app.crud.user import get_user_by_username_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import verify_password
from app.database.db import db_constructor
from pydantic import BaseModel
from app.auth.jwt import encode_jwt, decode_jwt

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


class ResponseToken(BaseModel):
    token: str
    token_type: str = "Bearer"


# Найти пользователя в БД
# Если нет → None
# Если есть → проверить пароль
# Если ок → вернуть user
# Если нет → None
async def authenticate_user(
    data_in: UserLoginSchema,
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user_db = await get_user_by_username_crud(data_in=data_in, session=session)
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин или пароль",
    )
    if user_db is None:
        raise unauthed_exc
    if not verify_password(
        password=data_in.password,
        hashed_password=user_db.password_hash,
    ):
        raise unauthed_exc
    return user_db


@router.post("/login", response_model=ResponseToken)
async def login(
    data_in: UserLoginSchema,
    session: AsyncSession = Depends(db_constructor.get_session),
    user: User = Depends(authenticate_user),
):
    data: dict = {}

    data.update(
        username=user.username,
        email=user.email,
        id=user.id,
    )
    create_access_token = encode_jwt(
        payload=data,
    )
    return ResponseToken(
        token=create_access_token,
    )
