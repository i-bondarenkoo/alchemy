from fastapi import FastAPI
import uvicorn
from app.core.config import settings

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server_run.host,
        port=settings.server_run.port,
    )
