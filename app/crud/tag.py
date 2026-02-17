from app.schemas.tag import CreateTagSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tag import Tag


async def create_tag_crud(tag_in: CreateTagSchema, session: AsyncSession):
    new_tag = Tag(**tag_in.model_dump())
    session.add(new_tag)
    await session.commit()
    await session.refresh(new_tag)
    return new_tag


async def get_tag_by_id_crud(tag_id: int, session: AsyncSession):
    return await session.get(Tag, tag_id)
