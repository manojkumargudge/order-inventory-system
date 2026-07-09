from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import require_admin
from src.db.session import get_db
from src.models.user import User
from src.repositories.admin_repository import AdminRepository
from src.schemas.dashboard import DashboardResponse
from src.schemas.order import OrderResponse
from src.schemas.product import ProductResponse
from src.schemas.user import UserRoleUpdate
from src.services.admin_service import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def get_admin_service(
    db: AsyncSession,
) -> AdminService:
    return AdminService(
        AdminRepository(db),
    )


@router.get(
    "/orders",
    response_model=list[OrderResponse],
)
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    """
    Get all orders (Admin only).
    """

    service = get_admin_service(db)

    return await service.get_all_orders()


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
)
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    """
    Get order by ID (Admin only).
    """

    service = get_admin_service(db)

    order = await service.get_order_by_id(order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    return order


@router.get(
    "/dashboard",
    response_model=DashboardResponse,
)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    """
    Get dashboard statistics (Admin only).
    """

    service = get_admin_service(db)

    return await service.get_dashboard_stats()


@router.get(
    "/inventory/low-stock",
    response_model=list[ProductResponse],
)
async def get_low_stock_products(
    threshold: int = Query(
        default=10,
        ge=0,
        description="Low stock threshold",
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    """
    Get products with low stock.
    """

    service = get_admin_service(db)

    return await service.get_low_stock_products(threshold)


@router.get(
    "/inventory/out-of-stock",
    response_model=list[ProductResponse],
)
async def get_out_of_stock_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    """
    Get products that are out of stock.
    """

    service = get_admin_service(db)

    return await service.get_out_of_stock_products()


@router.patch(
    "/products/{product_id}/restock",
    response_model=ProductResponse,
)
async def restock_product(
    product_id: int,
    quantity: int = Query(
        ...,
        gt=0,
        description="Quantity to add",
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    """
    Increase product stock.
    """

    service = get_admin_service(db)

    product = await service.restock_product(
        product_id,
        quantity,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@router.patch(
    "/users/{user_id}/role",
)
async def change_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    """
    Change a user's role.
    """

    service = get_admin_service(db)

    try:
        user = await service.change_user_role(
            current_user.id,
            user_id,
            role_data.role,
        )

        return {
            "message": "User role updated successfully.",
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )