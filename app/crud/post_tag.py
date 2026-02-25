from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post_tag import PostTag
from app.models.post import Post
from app.models.tag import Tag


async def create_post_tag_crud(post_id: int, tag_id: int, session: AsyncSession):
    post = await session.get(Post, post_id)
    if post is None:
        return "post_not_found"
    tag = await session.get(Tag, tag_id)
    if tag is None:
        return "tag_not_found"
    new_row = PostTag(
        post_id=post_id,
        tag_id=tag_id,
    )
    session.add(new_row)
    await session.commit()
    await session.refresh(new_row)
    return {"message": "Тэг добавлен к посту"}
