from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base_model import BaseModel


class Product(BaseModel):
    """
    Product model representing items in the inventory.
    """

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )