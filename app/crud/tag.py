from app.schemas.tag import CreateTagSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tag import Tag
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def create_tag_crud(tag_in: CreateTagSchema, session: AsyncSession):
    new_tag = Tag(**tag_in.model_dump())
    session.add(new_tag)
    await session.commit()
    await session.refresh(new_tag)
    return new_tag


async def get_tag_by_id_crud(tag_id: int, session: AsyncSession):
    return await session.get(Tag, tag_id)


async def get_tag_with_posts_crud(tag_id: int, session: AsyncSession):
    stmt = (
        select(Tag)
        .where(Tag.id == tag_id)
        .options(
            selectinload(Tag.posts),
        )
    )
    result = await session.execute(stmt)
    tag = result.scalars().one_or_none()
    if tag is None:
        return None
    return tag
