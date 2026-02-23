from app.schemas.user import (
    CreateUserSchema,
    PatchUpdateUserSchema,
    FullUpdateUserSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.post import Post
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from fastapi import Depends, HTTPException, status
from app.database.db import db_constructor


async def create_user_crud(user_in: CreateUserSchema, session: AsyncSession) -> User:
    new_user = User(**user_in.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_id_crud(user_id: int, session: AsyncSession):
    user = await session.get(User, user_id)
    return user


async def get_list_users_crud(session: AsyncSession, start: int = 0, stop: int = 3):
    stmt = select(User).order_by(User.id).limit(stop - start).offset(start)
    result = await session.execute(stmt)
    users: list = result.scalars().all()
    return users


async def delete_user_crud(user_id: int, session: AsyncSession):
    user = await session.get(User, user_id)
    if user is None:
        return None
    await session.delete(user)
    await session.commit()
    return {"message": "Пользователь удален"}


async def get_user_with_posts_crud(user_id: int, session: AsyncSession):
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.posts),
        )
    )
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return user


async def get_user_with_profile_crud(user_id: int, session: AsyncSession):
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(
            joinedload(User.profile),
        )
    )
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return user


async def get_user_with_posts_and_posts_with_tags_crud(
    user_id: int, session: AsyncSession
):
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.posts).selectinload(Post.tags),
        )
    )
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user is None:
        return None
    return user


async def update_user_crud(
    user_in: PatchUpdateUserSchema | FullUpdateUserSchema,
    session: AsyncSession,
    user: User,
    partial: bool = False,
):
    user_data: dict = user_in.model_dump(exclude_unset=partial)
    if len(user_data) == 0:
        return "словарь пустой"
    for key, value in user_data.items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id_dep(
    user_id: int, session: AsyncSession = Depends(db_constructor.get_session)
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user is None:
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден",
            )
    return user
