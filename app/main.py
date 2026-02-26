from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.views.user import router as user_router
from app.views.post import router as post_router
from app.views.profile import router as profile_router
from app.views.tag import router as tag_router
from app.auth.auth_views import router as auth_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
app.include_router(profile_router)
app.include_router(tag_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_run.host,
        port=settings.server_run.port,
        reload=True,
    )
