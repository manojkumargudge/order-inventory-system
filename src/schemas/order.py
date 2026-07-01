from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    """
    Schema for a single item in an order request.
    """

    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    """
    Schema for creating a new order.
    """

    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    """
    Schema for returning order item details.
    """

    id: int
    product_id: int
    quantity: int
    price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    """
    Schema for returning order details.
    """

    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
    order_items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)