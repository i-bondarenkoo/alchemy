from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.models.user import User
from app.schemas.user import UserLoginSchema
from app.crud.user import get_user_by_username_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import verify_password
from app.database.db import db_constructor
from jwt.exceptions import ExpiredSignatureError
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


async def get_current_user(
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


def get_token_payload(token=Depends(http_bearer)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не валидный токен",
        )
    try:
        return decode_jwt(token.credentials)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не валидный токен",
        )


async def get_user_from_access_token(
    token_data: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    if token_data["type"] != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Нужно передать токен типа - access",
        )
    username = token_data["username"]
    data_in: UserLoginSchema = UserLoginSchema(username=username, password="")
    user = await get_user_by_username_crud(data_in=data_in, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не валидный токен",
        )
    return user


async def get_user_from_refresh_token(
    token_data: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    if token_data["type"] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Нужно передать токен типа - refresh",
        )
    username = token_data["sub"]
    data_in: UserLoginSchema = UserLoginSchema(username=username, password="")
    user = await get_user_by_username_crud(data_in=data_in, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не валидный токен",
        )
    return user


@router.post("/login/", response_model=ResponseToken)
async def login(
    user: User = Depends(get_current_user),
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
    user: User = Depends(get_user_from_refresh_token),
):

    access_token = create_access_token(
        user=user,
    )
    return ResponseToken(
        access_token=access_token,
    )


@router.get("/users/me", response_model=ResponseTokenData)
def user_info(
    user: User = Depends(get_user_from_access_token),
):
    return ResponseTokenData(
        username=user.username,
        email=user.email,
        id=user.id,
    )
