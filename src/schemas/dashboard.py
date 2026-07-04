from decimal import Decimal

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    """
    Dashboard statistics response.
    """

    total_orders: int
    pending_orders: int
    confirmed_orders: int
    shipped_orders: int
    delivered_orders: int
    cancelled_orders: int
    total_revenue: Decimal