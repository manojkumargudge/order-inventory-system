from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.core.enums import PaymentStatus
from src.db.session import get_db
from src.models.user import User
from src.repositories.order_repository import OrderRepository
from src.repositories.payment_repository import PaymentRepository
from src.schemas.payment import PaymentCreate, PaymentResponse
from src.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


def get_payment_service(
    db: AsyncSession,
) -> PaymentService:
    return PaymentService(
        payment_repository=PaymentRepository(db),
        order_repository=OrderRepository(db),
    )


@router.post(
    "/{order_id}",
    response_model=PaymentResponse,
    status_code=201,
)
async def create_payment(
    order_id: int,
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a payment for an order.
    """

    service = get_payment_service(db)

    return await service.create_payment(
        order_id,
        payment_data,
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get payment by ID.
    """

    service = get_payment_service(db)

    return await service.get_payment_by_id(
        payment_id
    )


@router.get(
    "/order/{order_id}",
    response_model=PaymentResponse,
)
async def get_payment_by_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get payment by order ID.
    """

    service = get_payment_service(db)

    return await service.get_payment_by_order_id(
        order_id
    )


@router.patch(
    "/{payment_id}/success",
    response_model=PaymentResponse,
)
async def mark_payment_success(
    payment_id: int,
    transaction_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark payment as successful.
    """

    service = get_payment_service(db)

    return await service.update_payment_status(
        payment_id,
        PaymentStatus.SUCCESS,
        transaction_id,
    )


@router.patch(
    "/{payment_id}/failed",
    response_model=PaymentResponse,
)
async def mark_payment_failed(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark payment as failed.
    """

    service = get_payment_service(db)

    return await service.update_payment_status(
        payment_id,
        PaymentStatus.FAILED,
    )


@router.patch(
    "/{payment_id}/refund",
    response_model=PaymentResponse,
)
async def refund_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark payment as refunded.
    """

    service = get_payment_service(db)

    return await service.update_payment_status(
        payment_id,
        PaymentStatus.REFUNDED,
    )