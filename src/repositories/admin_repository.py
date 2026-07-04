from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.enums import OrderStatus
from src.models.order import Order


class AdminRepository:
    """
    Repository for admin database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_all_orders(
        self,
    ) -> list[Order]:
        """
        Get all orders.
        """

        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.order_items)
            )
            .order_by(Order.created_at.desc())
        )

        return result.scalars().all()

    async def get_order_by_id(
        self,
        order_id: int,
    ) -> Order | None:
        """
        Get order by ID.
        """

        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.order_items)
            )
            .where(Order.id == order_id)
        )

        return result.scalar_one_or_none()

    async def get_dashboard_stats(
        self,
    ) -> dict:
        """
        Get dashboard statistics.
        """

        total_orders = await self.db.scalar(
            select(func.count()).select_from(Order)
        )

        pending_orders = await self.db.scalar(
            select(func.count()).where(
                Order.status == OrderStatus.PENDING
            )
        )

        confirmed_orders = await self.db.scalar(
            select(func.count()).where(
                Order.status == OrderStatus.CONFIRMED
            )
        )

        shipped_orders = await self.db.scalar(
            select(func.count()).where(
                Order.status == OrderStatus.SHIPPED
            )
        )

        delivered_orders = await self.db.scalar(
            select(func.count()).where(
                Order.status == OrderStatus.DELIVERED
            )
        )

        cancelled_orders = await self.db.scalar(
            select(func.count()).where(
                Order.status == OrderStatus.CANCELLED
            )
        )

        total_revenue = await self.db.scalar(
            select(func.sum(Order.total_amount)).where(
                Order.status == OrderStatus.DELIVERED
            )
        )

        return {
            "total_orders": total_orders or 0,
            "pending_orders": pending_orders or 0,
            "confirmed_orders": confirmed_orders or 0,
            "shipped_orders": shipped_orders or 0,
            "delivered_orders": delivered_orders or 0,
            "cancelled_orders": cancelled_orders or 0,
            "total_revenue": total_revenue or 0,
        }