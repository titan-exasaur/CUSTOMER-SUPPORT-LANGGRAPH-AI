from fastapi import FastAPI

from src.api.routes import router
from src.config.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }