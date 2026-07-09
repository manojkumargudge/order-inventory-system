from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.enums import OrderStatus
from src.models.order import Order
from src.models.product import Product
from src.models.user import User


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

    async def get_low_stock_products(
        self,
        threshold: int = 10,
    ) -> list[Product]:
        """
        Get products with stock less than or equal to the threshold.
        """

        result = await self.db.execute(
            select(Product)
            .where(Product.stock <= threshold)
            .order_by(Product.stock.asc())
        )

        return result.scalars().all()

    async def get_out_of_stock_products(
        self,
    ) -> list[Product]:
        """
        Get products with zero stock.
        """

        result = await self.db.execute(
            select(Product)
            .where(Product.stock == 0)
            .order_by(Product.name)
        )

        return result.scalars().all()

    async def restock_product(
        self,
        product_id: int,
        quantity: int,
    ) -> Product | None:
        """
        Increase the stock of a product.
        """

        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )

        product = result.scalar_one_or_none()

        if product is None:
            return None

        product.stock += quantity

        await self.db.commit()
        await self.db.refresh(product)

        return product

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Get a user by ID.
        """

        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def update_user_role(
        self,
        user: User,
    ) -> User:
        """
        Update a user's role.
        """

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user