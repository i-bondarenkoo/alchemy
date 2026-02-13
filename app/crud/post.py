from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import CreatePostSchema
from app.models.post import Post


async def create_post_crud(post_in: CreatePostSchema, session: AsyncSession):
    new_post = Post(**post_in.model_dump())
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post
