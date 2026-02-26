from pydantic_settings import BaseSettings
from pydantic import BaseModel


class ServerRunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class AuthJWT(BaseModel):
    key: str = "bd9ed92fa0d60c9a647b81765f4082b1"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 5


class Settings(BaseSettings):
    server_run: ServerRunConfig = ServerRunConfig()
    auth_jwt: AuthJWT = AuthJWT()
    url: str = "postgresql+asyncpg://user:bujhm123@localhost:5435/training"
    echo: bool = True


settings = Settings()
