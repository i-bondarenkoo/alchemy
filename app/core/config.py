from pydantic_settings import BaseSettings
from pydantic import BaseModel


class ServerRunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class Settings(BaseSettings):
    server_run: ServerRunConfig = ServerRunConfig()
    url: str = "postgresql+asyncpg://user:bujhm123@localhost:5435/training"
    echo: bool = True


settings = Settings()
