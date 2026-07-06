from fastapi import HTTPException, status

from src.core.enums import PaymentStatus
from src.repositories.order_repository import OrderRepository
from src.repositories.payment_repository import PaymentRepository
from src.schemas.payment import PaymentCreate


class PaymentService:
    """
    Business logic for payment operations.
    """

    def __init__(
        self,
        payment_repository: PaymentRepository,
        order_repository: OrderRepository,
    ):
        self.payment_repository = payment_repository
        self.order_repository = order_repository

    async def create_payment(
        self,
        order_id: int,
        payment_data: PaymentCreate,
    ):
        """
        Create a payment for an order.
        """

        order = await self.order_repository.get_order_by_id(
            order_id
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        existing_payment = (
            await self.payment_repository.get_payment_by_order_id(
                order_id
            )
        )

        if existing_payment is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already exists for this order.",
            )

        return await self.payment_repository.create_payment(
            order,
            payment_data.payment_method,
        )

    async def get_payment_by_id(
        self,
        payment_id: int,
    ):
        """
        Get payment by ID.
        """

        payment = await self.payment_repository.get_payment_by_id(
            payment_id
        )

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found.",
            )

        return payment

    async def get_payment_by_order_id(
        self,
        order_id: int,
    ):
        """
        Get payment by order ID.
        """

        payment = (
            await self.payment_repository.get_payment_by_order_id(
                order_id
            )
        )

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found.",
            )

        return payment

    async def update_payment_status(
        self,
        payment_id: int,
        status: PaymentStatus,
        transaction_id: str | None = None,
    ):
        """
        Update payment status.
        """

        payment = await self.payment_repository.get_payment_by_id(
            payment_id
        )

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found.",
            )

        return await self.payment_repository.update_payment_status(
            payment,
            status,
            transaction_id,
        )