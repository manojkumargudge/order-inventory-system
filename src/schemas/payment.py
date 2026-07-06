from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import PaymentStatus


class PaymentCreate(BaseModel):
    """
    Schema for creating a payment.
    """

    payment_method: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )


class PaymentUpdate(BaseModel):
    """
    Schema for updating payment details.
    """

    status: PaymentStatus


class PaymentResponse(BaseModel):
    """
    Payment information returned by the API.
    """

    id: int
    order_id: int
    amount: float
    status: PaymentStatus
    payment_method: str
    transaction_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )