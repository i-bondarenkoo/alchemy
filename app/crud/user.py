from app.schemas.user import CreateUserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload


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
            joinedload(User.posts),
        )
    )
    result = await session.execute(stmt)
    user = result.unique().scalars().one_or_none()
    return user
