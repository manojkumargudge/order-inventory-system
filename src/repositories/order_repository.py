from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.order import Order
from src.models.order_item import OrderItem


class OrderRepository:
    """
    Repository class responsible for all Order database operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order: Order) -> Order:
        """
        Create a new order.
        """
        self.db.add(order)
        await self.db.flush()
        await self.db.refresh(order)
        return order

    async def create_order_item(self, order_item: OrderItem) -> OrderItem:
        """
        Create a new order item.
        """
        self.db.add(order_item)
        await self.db.flush()
        return order_item

    async def save(self, order: Order) -> Order:
        """
        Save changes to an existing order.
        """

        await self.db.flush()
        await self.db.refresh(order)

        return order

    async def get_order_by_id(self, order_id: int) -> Order | None:
        """
        Fetch a single order along with its items.
        """
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.order_items))
            .where(Order.id == order_id)
        )

        return result.scalar_one_or_none()

    async def get_order_by_id_and_user(
        self,
        order_id: int,
        user_id: int,
    ) -> Order | None:
        """
        Fetch an order belonging to a specific user.
        """

        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.order_items))
            .where(
                Order.id == order_id,
                Order.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_orders_by_user(self, user_id: int) -> list[Order]:
        """
        Fetch all orders belonging to a user.
        """
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.order_items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )

        return list(result.scalars().all())