from fastapi import APIRouter, Depends, Body, HTTPException, status
from app.schemas.profile import CreateProfileSchema, ResponseProfileSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import db_constructor
from app.crud.profile import create_profile_crud, get_profile_crud
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
    profile = await get_profile_crud(user_id=profile_in.user_id, session=session)
    if profile is None:
        return await create_profile_crud(profile_in=profile_in, session=session)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось создать профиль пользователя, вероятно он уже существует",
    )
