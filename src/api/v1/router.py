from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.products import router as product_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(product_router)