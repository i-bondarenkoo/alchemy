from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.tag import ResponseTagForRelationship

    # from app.schemas.post import ResponsePostSchemaForRelation
    from app.schemas.post import ResponsePostWithUser
# class CreatePostTagSchema(BaseModel):
#     post_id: int
#     tag_id: int


class ResponsePostTagSchemaForRelation(BaseModel):
    id: int
    # post_id: int
    # tag_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    tag: "ResponseTagForRelationship"


class ResponsePostTagSchemaForPost(BaseModel):
    id: int
    # post_id: int
    # tag_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    post: "ResponsePostWithUser"
