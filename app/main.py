from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.views.user import router as user_router

app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_run.host,
        port=settings.server_run.port,
        reload=True,
    )
