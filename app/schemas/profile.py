from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)
