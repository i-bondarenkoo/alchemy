from pydantic import BaseModel, ConfigDict
from app.schemas.user import ResponseUserForOtherRelationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.schemas.user import ResponseUserForOtherRelationship


class CreatePostSchema(BaseModel):
    user_id: int
    body: str | None = None
    title: str


class ResponsePostSchema(CreatePostSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class ResponsePostSchemaForRelation(BaseModel):
    id: int
    body: str | None = None
    title: str


class ResponsePostWithUser(BaseModel):
    id: int
    body: str | None = None
    title: str
    user: "ResponseUserForOtherRelationship"
