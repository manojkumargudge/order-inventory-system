from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import (
    get_current_user,
    require_admin,
)
from src.db.session import get_db
from src.models.user import User
from src.repositories.product_repository import ProductRepository
from src.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from src.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    print("\n" + "=" * 60)
    print("🔥 CREATE PRODUCT ENDPOINT EXECUTED")
    print(f"Username      : {current_user.username}")
    print(f"Role          : {current_user.role}")
    print(f"Superuser     : {current_user.is_superuser}")
    print("=" * 60 + "\n")

    repository = ProductRepository(db)
    service = ProductService(repository)

    try:
        return await service.create_product(product_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[ProductResponse],
)
async def get_all_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ProductRepository(db)
    service = ProductService(repository)

    return await service.get_all_products()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
async def get_product_by_id(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = ProductRepository(db)
    service = ProductService(repository)

    product = await service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    repository = ProductRepository(db)
    service = ProductService(repository)

    product = await service.update_product(
        product_id,
        product_data,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin()),
):
    repository = ProductRepository(db)
    service = ProductService(repository)

    deleted = await service.delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return {
        "message": "Product deleted successfully."
    }