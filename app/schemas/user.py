from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr


class ResponseUserSchema(CreateUserSchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
