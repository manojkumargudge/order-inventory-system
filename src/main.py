from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade Order & Inventory Management System",
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
    }