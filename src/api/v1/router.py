from fastapi import APIRouter

from src.api.v1.admin import router as admin_router
from src.api.v1.auth import router as auth_router
from src.api.v1.customers import router as customer_router
from src.api.v1.orders import router as order_router
from src.api.v1.products import router as product_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(product_router)
api_router.include_router(order_router)
api_router.include_router(customer_router)
api_router.include_router(admin_router)