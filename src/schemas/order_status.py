from pydantic import BaseModel

from src.models.enums import OrderStatus


class OrderStatusUpdate(BaseModel):
    """
    Request schema for updating an order status.
    """

    status: OrderStatus