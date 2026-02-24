from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import CreatePostSchema
from app.models.post import Post
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from fastapi import status, HTTPException

# from sqlalchemy import insert
# from app.models.post_tag import association_table
from app.models.tag import Tag
from app.models.post_tag import PostTag
from app.crud.tag import get_tag_by_id_crud


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


# async def add_tag_to_post_crud(post_id: int, tag_id: int, session: AsyncSession):
#     d_values = {
#         "tag_id": tag_id,
#         "post_id": post_id,
#     }
#     stmt = insert(association_table).values(d_values)
#     await session.execute(stmt)
#     await session.commit()
#     return {"message": "данные добавлены"}


# async def add_tag_to_post_crud(post_id: int, tag_id: int, session: AsyncSession):
#     stmt = (
#         select(Post)
#         .where(Post.id == post_id)
#         .options(
#             selectinload(
#                 Post.tags,
#             )
#         )
#     )
#     result = await session.execute(stmt)
#     post = result.scalars().one_or_none()
#     if post is None:
#         return "post_not_found"
#     tag = await session.get(Tag, tag_id)
#     if tag is None:
#         return "tag_not_found"
#     if tag in post.tags:
#         return None
#     post.tags.append(tag)
#     await session.commit()
#     return {"message": "Тэг добавлен к посту"}
async def add_tag_to_post_crud(
    post_id: int,
    tag_id: int,
    session: AsyncSession,
):
    stmt = (
        select(Post)
        .where(Post.id == post_id)
        .options(selectinload(Post.tags).joinedload(PostTag.tag))
    )
    result = await session.execute(stmt)
    post = result.scalars().one_or_none()
    if post is None:
        return "post_not_found"
    tag = await get_tag_by_id_crud(tag_id=tag_id, session=session)
    if tag is None:
        return "tag_not_found"
    # for id_tag in post.tags:
    #     if id_tag == tag_id:
    #         return "связка идентификаторов уже существует"
    #     data = (post_id, tag_id)
    #     post.tags.append(data)
    post.tags.append(tag.id)
    await session.commit()

    return {"message": "Тэг добавлен к посту"}


async def get_post_with_tags_crud(post_id: int, session: AsyncSession):
    stmt = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(
                Post.tags,
            )
        )
    )
    result = await session.execute(stmt)
    post = result.scalars().one_or_none()
    return post
