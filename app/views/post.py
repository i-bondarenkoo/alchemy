from sqlalchemy.ext.asyncio import AsyncSession
from app.database import db_constructor
from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from app.schemas.post import CreatePostSchema, ResponsePostSchema
from app.crud.user import get_user_by_id_crud
from app.crud.post import create_post_crud

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("/", response_model=ResponsePostSchema)
async def create_post(
    post_in: Annotated[CreatePostSchema, Body(description="Данные поста")],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    user = await get_user_by_id_crud(user_id=post_in.user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return await create_post_crud(post_in=post_in, session=session)
