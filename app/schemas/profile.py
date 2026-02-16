from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.schemas.user import ResponseUserForOtherRelationship


class CreateProfileSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    user_id: int


class ResponseProfileSchema(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseProfileRelationForUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    # id: int
    # user_id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseProfileWithUser(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    user: "ResponseUserForOtherRelationship"
