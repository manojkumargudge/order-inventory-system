from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.core.enums import InventoryTransactionType


class InventoryTransactionBase(BaseModel):
    """
    Base schema for inventory transactions.
    """

    product_id: int
    quantity: int
    transaction_type: InventoryTransactionType
    remarks: str | None = None


class InventoryTransactionCreate(InventoryTransactionBase):
    """
    Schema used when creating
    an inventory transaction.
    """

    pass


class InventoryTransactionResponse(InventoryTransactionBase):
    """
    Schema returned to clients.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )