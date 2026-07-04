from pydantic import BaseModel

from src.core.enums import OrderStatus


class OrderStatusUpdate(BaseModel):
    """
    Schema for updating an order status.
    """

    status: OrderStatus