from app.crud.tag import create_tag_crud, get_tag_by_id_crud, get_tag_with_posts_crud
from fastapi import APIRouter, Body, HTTPException, Path, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.tag import CreateTagSchema, ResponseTagSchema, ResponseTagWithPosts
from app.database.db import db_constructor
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.post("/", response_model=ResponseTagSchema)
async def create_tag(
    tag_in: Annotated[CreateTagSchema, Body(description="Данные для создания тэга")],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    try:
        tag = await create_tag_crud(tag_in=tag_in, session=session)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тэг с таким именем уже существует",
        )
    return tag


@router.get("/{tag_id}", response_model=ResponseTagSchema)
async def get_tag_by_id(
    tag_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    tag = await get_tag_by_id_crud(tag_id=tag_id, session=session)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тэг не найден",
        )
    return tag


@router.get("/{tag_id}/posts", response_model=ResponseTagWithPosts)
async def get_tag_with_posts(
    tag_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    tag = await get_tag_with_posts_crud(tag_id=tag_id, session=session)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тэг не найден",
        )
    return tag
