from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class OrderStatus:
    """
    Order status constants.
    """

    PENDING = "PENDING"
    CANCELLED = "CANCELLED"


class Order(BaseModel):
    """
    Order model representing a customer's order.
    """

    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default=OrderStatus.PENDING,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="orders",
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )