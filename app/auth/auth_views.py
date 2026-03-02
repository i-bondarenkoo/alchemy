from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.models.user import User
from app.schemas.user import UserLoginSchema
from app.crud.user import get_user_by_username_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import verify_password
from app.database.db import db_constructor
from pydantic import BaseModel
from app.auth.jwt import encode_jwt, decode_jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class ResponseToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"


def create_pd_model(username: str, password: str) -> UserLoginSchema:
    return UserLoginSchema(
        username=username,
        password=password,
    )


async def authenticate_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    data_in: UserLoginSchema = create_pd_model(
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


def create_access_token(
    user: User,
):
    user_data: dict = {}
    user_data.update(
        username=user.username,
        email=user.email,
        id=user.id,
    )
    token = encode_jwt(
        payload=user_data,
    )
    return ResponseToken(
        access_token=token,
    )


def decode_token(token: str):
    data: dict = decode_jwt(token)
    return {
        "username": data["username"],
        "email": data["email"],
        "id": data["id"],
    }


@router.post("/login", response_model=ResponseToken)
async def login(
    user: User = Depends(authenticate_user),
):
    return create_access_token(user)


@router.get("/users/me")
async def check_auth_user(
    token: str = Depends(oauth2_scheme),
    # token: str,
):
    try:
        return decode_token(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не верный токен",
        )
