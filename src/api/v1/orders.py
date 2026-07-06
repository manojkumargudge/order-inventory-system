from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.db.session import get_db
from src.models.user import User
from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository
from src.schemas.order import OrderCreate, OrderResponse
from src.services.order_service import OrderService
from src.core.enums import OrderStatus

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


def get_order_service(
    db: AsyncSession = Depends(get_db),
) -> OrderService:
    order_repository = OrderRepository(db)
    product_repository = ProductRepository(db)

    return OrderService(
        order_repository,
        product_repository,
    )


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    try:
        return await order_service.create_order(
            current_user.id,
            order_data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    order = await order_service.get_order_by_id(
        order_id,
        current_user.id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    return order


@router.get(
    "",
    response_model=list[OrderResponse],
)
async def get_orders(
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.get_orders_by_user(
        current_user.id,
    )


@router.patch(
    "/{order_id}/cancel",
    response_model=OrderResponse,
)
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    try:
        order = await order_service.cancel_order(
            order_id,
            current_user.id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        return order

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
)
async def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
):
    try:
        order = await order_service.update_order_status(
            order_id,
            current_user.id,
            new_status,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        return order

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )