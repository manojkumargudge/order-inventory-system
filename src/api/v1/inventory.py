from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.repositories.inventory_repository import InventoryRepository
from src.repositories.product_repository import ProductRepository
from src.schemas.inventory_transaction import (
    InventoryTransactionCreate,
    InventoryTransactionResponse,
)
from src.services.inventory_service import InventoryService

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


def get_inventory_service(
    db: AsyncSession = Depends(get_db),
) -> InventoryService:
    """
    Dependency to provide InventoryService.
    """

    inventory_repository = InventoryRepository(db)
    product_repository = ProductRepository(db)

    return InventoryService(
        inventory_repository=inventory_repository,
        product_repository=product_repository,
    )


@router.post(
    "/transactions",
    response_model=InventoryTransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory_transaction(
    transaction_data: InventoryTransactionCreate,
    service: InventoryService = Depends(
        get_inventory_service
    ),
):
    """
    Record an inventory transaction.
    """

    try:
        return await service.record_transaction(
            transaction_data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )