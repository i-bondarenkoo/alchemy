from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.models.user import User
from app.schemas.user import UserLoginSchema
from app.crud.user import get_user_by_username_crud, get_user_by_id_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import verify_password
from app.database.db import db_constructor

from fastapi.security import HTTPBearer
from app.auth.schemas import ResponseToken
from app.auth.helpers_jwt import (
    create_access_token,
    create_refresh_token,
    validate_token_type,
)
from app.auth.jwt import decode_jwt
from app.auth.schemas import ResponseTokenData

http_bearer = HTTPBearer(auto_error=False)

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


@router.post("/login", response_model=ResponseToken)
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
async def refrest_jwt_token(
    session: AsyncSession = Depends(db_constructor.get_session),
    token=Depends(http_bearer),
):
    token = token.credentials
    if validate_token_type(token) == "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Для получения access токена нужен валидный refresh токен",
        )
    decode_token: dict = decode_jwt(token)
    current_user: User = await get_user_by_id_crud(
        user_id=decode_token["id"],
        session=session,
    )
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
        )
    new_access_token = create_access_token(user=current_user)
    return ResponseToken(
        access_token=new_access_token,
    )


@router.get("/users/me")
async def check_auth_user(
    token: str = Depends(http_bearer),
):
    # info = validate_token_type(token)
    # if not info:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Для получения нинформации о пользователе нужнен тип токена - access",
    #     )
    # user = decode_jwt(token)
    # return ResponseTokenData(
    #     usernmae=user["username"],
    #     email=user["email"],
    #     type=user["type"],
    # )
    pass
