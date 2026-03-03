from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.models.user import User
from app.schemas.user import UserLoginSchema
from app.crud.user import get_user_by_username_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import verify_password
from app.database.db import db_constructor

from fastapi.security import HTTPBearer
from app.auth.schemas import ResponseToken
from app.auth.helpers_jwt import (
    create_access_token,
    create_refresh_token,
)
from app.auth.jwt import decode_jwt
from app.auth.schemas import ResponseTokenData

http_bearer = HTTPBearer(auto_error=False)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


async def authenticate_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    data_in: UserLoginSchema = UserLoginSchema(
        username=username,
        password=password,
    )
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


@router.post("/login/", response_model=ResponseToken)
async def login(
    user: User = Depends(authenticate_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return ResponseToken(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh/",
    response_model=ResponseToken,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    token=Depends(http_bearer),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    token_str = token.credentials
    token_decode: dict = decode_jwt(token_str)
    if token_decode["type"] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Для получения нового access токена нужен валидный refresh токен",
        )
    username_for_token: str = token_decode["sub"]
    data_in: UserLoginSchema = UserLoginSchema(
        username=username_for_token,
        password="",
    )
    user = await get_user_by_username_crud(data_in=data_in, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не валидный токен",
        )
    access_token = create_access_token(
        user=user,
    )
    return ResponseToken(
        access_token=access_token,
    )


@router.get("/users/me")
def user_info(
    token=Depends(http_bearer),
):
    token_str: str = token.credentials
    token_decode: dict = decode_jwt(token_str)
    if token_decode["type"] != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не валидный токен",
        )
    return ResponseTokenData(
        username=token_decode["username"],
        email=token_decode["email"],
        id=token_decode["id"],
    )
