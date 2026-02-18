from pydantic import BaseModel, ConfigDict

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.post import ResponsePostSchemaForRelation


class CreateTagSchema(BaseModel):
    name: str
    color: str | None = None


class ResponseTagSchema(CreateTagSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseTagForRelationship(CreateTagSchema):
    model_config = ConfigDict(from_attributes=True)


class ResponseTagWithPosts(CreateTagSchema):
    posts: list["ResponsePostSchemaForRelation"]
    model_config = ConfigDict(from_attributes=True)
