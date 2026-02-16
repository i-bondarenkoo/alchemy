from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.profile import CreateProfileSchema
from app.models.profile import Profile
from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def create_profile_crud(
    profile_in: CreateProfileSchema,
    session: AsyncSession,
):
    new_profile = Profile(**profile_in.model_dump())
    session.add(new_profile)
    await session.commit()
    await session.refresh(new_profile)
    return new_profile


async def get_profile_by_id_crud(profile_id: int, session: AsyncSession):
    stmt = select(Profile).where(Profile.id == profile_id)
    result = await session.execute(stmt)
    profile = result.scalars().one_or_none()
    return profile


async def get_profile_with_user_crud(profile_id: int, session: AsyncSession):
    stmt = (
        select(Profile)
        .where(Profile.id == profile_id)
        .options(
            joinedload(Profile.user),
        )
    )
    result = await session.execute(stmt)
    profile = result.scalars().one_or_none()
    return profile
