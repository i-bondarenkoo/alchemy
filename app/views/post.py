from sqlalchemy.ext.asyncio import AsyncSession
from app.database import db_constructor
from fastapi import APIRouter, Depends, Body, HTTPException, status, Path
from typing import Annotated
from app.schemas.post import CreatePostSchema, ResponsePostSchema, ResponsePostWithUser
from app.crud.user import get_user_by_id_crud
from app.crud.post import create_post_crud, get_post_with_user_crud, get_post_by_id_crud

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


@router.get("/{post_id}", response_model=ResponsePostSchema)
async def get_post(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    post = await get_post_by_id_crud(post_id=post_id, session=session)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден",
        )
    return post


@router.get("/{post_id}/users", response_model=ResponsePostWithUser)
async def get_post_with_user(
    post_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    post = await get_post_with_user_crud(post_id=post_id, session=session)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден",
        )
    return post
