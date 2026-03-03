from pydantic import BaseModel, EmailStr


class ResponseToken(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class ResponseTokenData(BaseModel):
    username: str
    email: EmailStr
    type: str
