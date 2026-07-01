from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base_model import BaseModel


class OrderItem(BaseModel):
    """
    Order item model representing a single product within an order.
    """

    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    order = relationship(
        "Order",
        back_populates="order_items",
    )

    product = relationship(
        "Product",
        back_populates="order_items",
    )