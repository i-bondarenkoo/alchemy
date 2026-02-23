from fastapi import APIRouter, Body, Depends, HTTPException, Query, status, Path

from app.schemas.user import (
    CreateUserSchema,
    ResponseUserSchema,
    ResponseUserSchemaWithPosts,
    ResponseUserSchemaWithProfiles,
    ResponseUserWithPostAndTags,
    PatchUpdateUserSchema,
    FullUpdateUserSchema,
)
from app.models.user import User
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import db_constructor
from app.crud.user import (
    create_user_crud,
    delete_user_crud,
    get_list_users_crud,
    get_user_by_id_crud,
    get_user_with_posts_crud,
    get_user_with_profile_crud,
    get_user_with_posts_and_posts_with_tags_crud,
    update_user_crud,
    get_user_by_id_dep,
)
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
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
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


@router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(ge=1, description="ID пользователя для удаления")],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user = await delete_user_crud(user_id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user


@router.get("/{user_id}/posts", response_model=ResponseUserSchemaWithPosts)
async def get_user_with_posts(
    user_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user = await get_user_with_posts_crud(user_id=user_id, session=session)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    return user


@router.get("/{user_id}/profiles", response_model=ResponseUserSchemaWithProfiles)
async def get_user_with_profile(
    user_id: Annotated[int, Path(ge=1, description=("ID Пользователя"))],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user = await get_user_with_profile_crud(user_id=user_id, session=session)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )
    return user


@router.get("/{user_id}/all", response_model=ResponseUserWithPostAndTags)
async def get_user_with_posts_and_posts_with_tags(
    user_id: Annotated[int, Path(ge=1, description=("ID Пользователя"))],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user = await get_user_with_posts_and_posts_with_tags_crud(
        user_id=user_id,
        session=session,
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )
    return user


@router.patch("/{user_id}", response_model=ResponseUserSchema)
async def patch_update_user(
    user_in: Annotated[
        PatchUpdateUserSchema, Body(description="данные для обновления")
    ],
    session: AsyncSession = Depends(db_constructor.get_session),
    user: User = Depends(get_user_by_id_dep),
):

    update_user = await update_user_crud(
        user_in=user_in,
        session=session,
        partial=True,
        user=user,
    )
    if update_user == "словарь пустой":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не передали",
        )
    return update_user


@router.put("/{user_id}", response_model=ResponseUserSchema)
async def full_update_user(
    user_in: Annotated[FullUpdateUserSchema, Body(description="данные для обновления")],
    user: User = Depends(get_user_by_id_dep),
    session: AsyncSession = Depends(db_constructor.get_session),
):

    update_user = await update_user_crud(
        user_in=user_in,
        session=session,
        partial=False,
        user=user,
    )
    if update_user == "словарь пустой":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не передали",
        )
    return update_user
