from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from app.schemas.post import ResponsePostSchemaForRelation
from typing import TYPE_CHECKING


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
