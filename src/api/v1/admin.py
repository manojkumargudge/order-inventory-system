from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.db.session import get_db
from src.models.user import User
from src.repositories.admin_repository import AdminRepository
from src.schemas.dashboard import DashboardResponse
from src.schemas.order import OrderResponse
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
    current_user: User = Depends(get_current_user),
):
    """
    Get all orders (Admin only).
    """

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    service = get_admin_service(db)

    return await service.get_all_orders()


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
)
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get order by ID (Admin only).
    """

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

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
    current_user: User = Depends(get_current_user),
):
    """
    Get dashboard statistics (Admin only).
    """

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    service = get_admin_service(db)

    return await service.get_dashboard_stats()