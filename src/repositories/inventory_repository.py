from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.inventory_transaction import InventoryTransaction


class InventoryRepository:
    """
    Repository for inventory transaction database operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_transaction(
        self,
        transaction: InventoryTransaction,
    ) -> InventoryTransaction:
        """
        Create a new inventory transaction.
        """

        self.db.add(transaction)
        await self.db.flush()
        await self.db.refresh(transaction)

        return transaction

    async def get_by_id(
        self,
        transaction_id: int,
    ) -> InventoryTransaction | None:
        """
        Get a single inventory transaction by ID.
        """

        return await self.db.get(
            InventoryTransaction,
            transaction_id,
        )

    async def get_transaction_by_id(
        self,
        transaction_id: int,
    ) -> InventoryTransaction | None:
        """
        Alias for fetching a single transaction by ID.
        """

        return await self.get_by_id(transaction_id)

    async def get_all(
        self,
    ) -> list[InventoryTransaction]:
        """
        Get all inventory transactions.
        """

        result = await self.db.execute(
            select(InventoryTransaction)
            .order_by(InventoryTransaction.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_transactions(
        self,
    ) -> list[InventoryTransaction]:
        """
        Get all inventory transactions.
        """

        return await self.get_all()

    async def get_product_transactions(
        self,
        product_id: int,
    ) -> list[InventoryTransaction]:
        """
        Get all transactions for a product.
        """

        result = await self.db.execute(
            select(InventoryTransaction)
            .where(InventoryTransaction.product_id == product_id)
            .order_by(InventoryTransaction.created_at.desc())
        )

        return list(result.scalars().all())