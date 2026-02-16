from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import CreatePostSchema
from app.models.post import Post
from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def create_post_crud(post_in: CreatePostSchema, session: AsyncSession):
    new_post = Post(**post_in.model_dump())
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


async def get_post_by_id_crud(post_id: int, session: AsyncSession):
    return await session.get(Post, post_id)


async def get_post_with_user_crud(post_id: int, session: AsyncSession):
    stmt = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            joinedload(Post.user),
        )
    )
    result = await session.execute(stmt)
    post = result.scalars().one_or_none()
    return post
