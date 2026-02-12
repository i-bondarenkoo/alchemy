from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Path
from app.schemas.user import CreateUserSchema, ResponseUserSchema
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import db_constructor
from app.crud.user import create_user_crud, get_list_users_crud, get_user_by_id_crud
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=ResponseUserSchema)
async def create_user(
    user_in: Annotated[
        CreateUserSchema,
        Body(description="Данные для создания пользователя"),
    ],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    try:
        user = await create_user_crud(user_in=user_in, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username или email уже существует",
        )
    return user


@router.get("/{user_id}", response_model=ResponseUserSchema)
async def get_user_by_id(
    user_id: Annotated[int, Path(ge=1, description="ID пользователя")],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user = await get_user_by_id_crud(user_id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user


@router.get("/", response_model=list[ResponseUserSchema])
async def get_list_users(
    start: int = Query(0, ge=0, description="Начальный диапазон списка пользователей"),
    stop: int = Query(3, gt=1, description="Конечный диапазон списка пользователей"),
    session: AsyncSession = Depends(db_constructor.get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Начальный диапазон, для списка, не может быть больше конечного",
        )
    return await get_list_users_crud(start=start, stop=stop, session=session)
