from pydantic import BaseModel, ConfigDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.post import ResponsePostWithUser

    # from app.schemas.post import ResponsePostSchemaForRelation
    from app.schemas.post_tag import (
        ResponsePostTagSchemaForPost,
        ResponsePostTagSchemaForRelation,
    )


class CreateTagSchema(BaseModel):
    name: str
    color: str | None = None


class ResponseTagSchema(CreateTagSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseTagForRelationship(CreateTagSchema):
    model_config = ConfigDict(from_attributes=True)


# class ResponseTagWithPosts(CreateTagSchema):
#     posts: list["ResponsePostSchemaForRelation"]
#     model_config = ConfigDict(from_attributes=True)


class ResponseTagWithPosts(CreateTagSchema):
    posts: list["ResponsePostTagSchemaForRelation"]
    model_config = ConfigDict(from_attributes=True)


# class ResponseTagWithPostsAndUser(BaseModel):
#     name: str
#     color: str | None = None
#     model_config = ConfigDict(from_attributes=True)
#     posts: list["ResponsePostWithUser"]


class ResponseTagWithPostsAndUser(BaseModel):
    name: str
    color: str | None = None
    model_config = ConfigDict(from_attributes=True)
    posts: list["ResponsePostTagSchemaForPost"]
