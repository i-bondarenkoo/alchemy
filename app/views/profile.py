from typing import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException, status, Path
from app.schemas.profile import (
    CreateProfileSchema,
    ResponseProfileSchema,
    ResponseProfileWithUser,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import db_constructor
from app.crud.profile import (
    create_profile_crud,
    get_profile_by_id_crud,
    get_profile_with_user_crud,
)
from app.crud.user import get_user_by_id_crud

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)


@router.post("/", response_model=ResponseProfileSchema)
async def create_profile(
    profile_in: CreateProfileSchema,
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user = await get_user_by_id_crud(user_id=profile_in.user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не существует",
        )
    profile = await get_profile_by_id_crud(user_id=profile_in.user_id, session=session)
    if profile is None:
        return await create_profile_crud(profile_in=profile_in, session=session)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось создать профиль пользователя, вероятно он уже существует",
    )


@router.get("/{profile_id}", response_model=ResponseProfileSchema)
async def get_profile_by_id(
    profile_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    profile = await get_profile_by_id_crud(
        profile_id=profile_id,
        session=session,
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не найден",
        )
    return profile


@router.get("{profile_id}/users", response_model=ResponseProfileWithUser)
async def get_profile_with_user(
    profile_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    profile = await get_profile_with_user_crud(profile_id=profile_id, session=session)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль не найден",
        )
    return profile
