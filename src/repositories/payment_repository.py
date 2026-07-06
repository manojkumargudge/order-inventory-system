from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import PaymentStatus
from src.models.order import Order
from src.models.payment import Payment


class PaymentRepository:
    """
    Repository for payment database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create_payment(
        self,
        order: Order,
        payment_method: str,
    ) -> Payment:
        """
        Create a payment for an order.
        """

        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method=payment_method,
            status=PaymentStatus.PENDING,
        )

        self.db.add(payment)

        await self.db.commit()
        await self.db.refresh(payment)

        return payment

    async def get_payment_by_id(
        self,
        payment_id: int,
    ) -> Payment | None:
        """
        Get payment by ID.
        """

        result = await self.db.execute(
            select(Payment).where(
                Payment.id == payment_id
            )
        )

        return result.scalar_one_or_none()

    async def get_payment_by_order_id(
        self,
        order_id: int,
    ) -> Payment | None:
        """
        Get payment by order ID.
        """

        result = await self.db.execute(
            select(Payment).where(
                Payment.order_id == order_id
            )
        )

        return result.scalar_one_or_none()

    async def update_payment_status(
        self,
        payment: Payment,
        status: PaymentStatus,
        transaction_id: str | None = None,
    ) -> Payment:
        """
        Update payment status.
        """

        payment.status = status

        if transaction_id is not None:
            payment.transaction_id = transaction_id

        await self.db.commit()
        await self.db.refresh(payment)

        return payment