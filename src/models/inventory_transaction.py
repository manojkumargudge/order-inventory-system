from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.enums import InventoryTransactionType
from src.models.base_model import BaseModel

if TYPE_CHECKING:
    from src.models.product import Product


class InventoryTransaction(BaseModel):
    """
    Stores every inventory stock movement for audit and reporting.
    """

    __tablename__ = "inventory_transactions"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    transaction_type: Mapped[InventoryTransactionType] = mapped_column(
        Enum(InventoryTransactionType),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        back_populates="inventory_transactions",
    )