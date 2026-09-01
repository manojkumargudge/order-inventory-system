from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from src.core.enums import (
    InventoryTransactionType,
    SortOrder,
)


class InventoryTransactionBase(BaseModel):
    """
    Base schema for inventory transactions.
    """

    product_id: int
    quantity: int
    transaction_type: InventoryTransactionType
    remarks: str | None = None


class InventoryTransactionCreate(
    InventoryTransactionBase
):
    """
    Schema used when creating
    an inventory transaction.
    """

    pass


class InventoryTransactionResponse(
    InventoryTransactionBase
):
    """
    Schema returned to clients.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class InventoryTransactionFilter(
    BaseModel
):
    """
    Filtering options for
    inventory transactions.
    """

    product_id: int | None = None

    transaction_type: (
        InventoryTransactionType | None
    ) = None

    from_date: date | None = None

    to_date: date | None = None

    page: int = 1

    page_size: int = 10

    sort_order: SortOrder = (
        SortOrder.DESC
    )


class InventorySummary(
    BaseModel
):
    """
    Inventory summary for
    a product.
    """

    product_id: int

    current_stock: int

    total_purchased: int

    total_sold: int

    total_returned: int

    total_damaged: int


class InventoryDashboard(
    BaseModel
):
    """
    Inventory dashboard
    statistics.
    """

    total_products: int

    low_stock_products: int

    out_of_stock_products: int

    total_transactions: int