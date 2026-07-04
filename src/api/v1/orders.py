from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.db.session import get_db
from src.models.enums import OrderStatus
from src.models.user import User
from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository
from src.schemas.order import OrderCreate, OrderResponse
from src.schemas.order_status import OrderStatusUpdate
from src.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


def get_order_service(
    db: AsyncSession,
) -> OrderService:
    return OrderService(
        OrderRepository(db),
        ProductRepository(db),
    )


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new order.
    """

    service = get_order_service(db)

    try:
        return await service.create_order(
            current_user.id,
            order_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[OrderResponse],
)
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all orders for the current user.
    """

    service = get_order_service(db)

    return await service.get_orders_by_user(
        current_user.id,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get an order by ID.
    """

    service = get_order_service(db)

    order = await service.get_order_by_id(
        order_id,
        current_user.id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    return order


@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
)
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel an order.
    """

    service = get_order_service(db)

    try:
        order = await service.cancel_order(
            order_id,
            current_user.id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        return order

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the status of an order.
    """

    service = get_order_service(db)

    try:
        order = await service.update_order_status(
            order_id,
            current_user.id,
            status_update.status,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        return order

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )