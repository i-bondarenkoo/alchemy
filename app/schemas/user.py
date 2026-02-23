from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from app.schemas.profile import ResponseProfileRelationForUser
    from app.schemas.post import ResponsePostSchemaForRelation, ResponsePostWithTags


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr


class ResponseUserSchema(CreateUserSchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponseUserSchemaWithPosts(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: list["ResponsePostSchemaForRelation"]
    model_config = ConfigDict(from_attributes=True)


class ResponseUserSchemaWithProfiles(BaseModel):
    id: int
    username: str
    email: EmailStr
    profile: Optional["ResponseProfileRelationForUser"] = None
    model_config = ConfigDict(from_attributes=True)


class ResponseUserForOtherRelationship(BaseModel):
    # id: int
    username: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResponseUserWithPostAndTags(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: list["ResponsePostWithTags"]


class PatchUpdateUserSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class FullUpdateUserSchema(BaseModel):
    username: str
    email: EmailStr
