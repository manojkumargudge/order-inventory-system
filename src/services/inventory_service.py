from src.core.enums import InventoryTransactionType
from src.models.inventory_transaction import InventoryTransaction
from src.repositories.inventory_repository import (
    InventoryRepository,
)
from src.repositories.product_repository import (
    ProductRepository,
)
from src.schemas.inventory_transaction import (
    InventoryTransactionCreate,
)


class InventoryService:
    """
    Inventory business logic.
    """

    def __init__(
        self,
        inventory_repository: InventoryRepository,
        product_repository: ProductRepository,
    ):
        self.inventory_repository = inventory_repository
        self.product_repository = product_repository

    async def record_transaction(
        self,
        transaction_data: InventoryTransactionCreate,
    ) -> InventoryTransaction:
        """
        Record an inventory transaction
        and update product stock.
        """

        product = await self.product_repository.get_by_id(
            transaction_data.product_id
        )

        if product is None:
            raise ValueError(
                "Product not found."
            )

        if transaction_data.quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        stock_out_transactions = {
            InventoryTransactionType.SALE,
            InventoryTransactionType.DAMAGED,
        }

        if (
            transaction_data.transaction_type
            in stock_out_transactions
        ):
            if not await self.product_repository.has_sufficient_stock(
                product,
                transaction_data.quantity,
            ):
                raise ValueError(
                    "Insufficient stock."
                )

            await self.product_repository.decrease_stock(
                product,
                transaction_data.quantity,
            )

        else:
            await self.product_repository.increase_stock(
                product,
                transaction_data.quantity,
            )

        transaction = InventoryTransaction(
            **transaction_data.model_dump()
        )

        try:
            transaction = (
                await self.inventory_repository.create_transaction(
                    transaction
                )
            )

            await self.inventory_repository.db.commit()

            return transaction

        except Exception:
            await self.inventory_repository.db.rollback()
            raise

    async def get_transaction(
        self,
        transaction_id: int,
    ) -> InventoryTransaction | None:
        """
        Get inventory transaction by ID.
        """

        return await self.inventory_repository.get_transaction_by_id(
            transaction_id
        )

    async def get_transactions(
        self,
    ) -> list[InventoryTransaction]:
        """
        Get all inventory transactions.
        """

        return await self.inventory_repository.get_transactions()

    async def get_product_transactions(
        self,
        product_id: int,
    ) -> list[InventoryTransaction]:
        """
        Get all transactions
        for a product.
        """

        return await self.inventory_repository.get_product_transactions(
            product_id
        )