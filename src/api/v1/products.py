from decimal import Decimal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import (
    get_current_user,
    require_admin,
)
from src.core.enums import (
    ProductSortField,
    SortOrder,
)
from src.db.session import get_db
from src.models.user import User
from src.repositories.product_repository import ProductRepository
from src.schemas.inventory import StockUpdateRequest
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


# ======================================================
# Dependencies
# ======================================================

def get_product_service(
    db: AsyncSession = Depends(get_db),
) -> ProductService:
    """
    Return ProductService instance.
    """
    repository = ProductRepository(db)
    return ProductService(
        repository
    )


# ======================================================
# Create Product
# ======================================================

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate,
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        require_admin(),
    ),
):
    try:
        return await product_service.create_product(
            product_data
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ======================================================
# Get Products
# ======================================================

@router.get(
    "",
    response_model=list[ProductResponse],
)
async def get_products(
    search: str | None = Query(
        default=None,
        description="Search by product name or description.",
    ),
    min_price: Decimal | None = Query(
        default=None,
        ge=0,
    ),
    max_price: Decimal | None = Query(
        default=None,
        ge=0,
    ),
    in_stock: bool | None = Query(
        default=None,
    ),
    sort_by: ProductSortField | None = Query(
        default=None,
    ),
    order: SortOrder = Query(
        default=SortOrder.ASC,
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        get_current_user,
    ),
):
    return await product_service.get_products(
        search=search,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size,
    )


# ======================================================
# Low Stock Products
# ======================================================
# NOTE: Must be registered BEFORE "/{product_id}" — otherwise
# FastAPI matches "low-stock" as a product_id path value first
# and returns a 422 instead of reaching this route.

@router.get(
    "/low-stock",
    response_model=list[ProductResponse],
)
async def get_low_stock_products(
    threshold: int = Query(
        default=10,
        ge=0,
    ),
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        get_current_user,
    ),
):
    return await product_service.get_low_stock_products(
        threshold
    )


# ======================================================
# Out Of Stock Products
# ======================================================
# NOTE: Same reason as above — must precede "/{product_id}".

@router.get(
    "/out-of-stock",
    response_model=list[ProductResponse],
)
async def get_out_of_stock_products(
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        get_current_user,
    ),
):
    return await product_service.get_out_of_stock_products()


# ======================================================
# Get Product By ID
# ======================================================

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
async def get_product_by_id(
    product_id: int,
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        get_current_user,
    ),
):
    product = await product_service.get_product_by_id(
        product_id
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    return product


# ======================================================
# Update Product
# ======================================================

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        require_admin(),
    ),
):
    product = await product_service.update_product(
        product_id,
        product_data,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


# ======================================================
# Delete Product
# ======================================================

@router.delete(
    "/{product_id}",
)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        require_admin(),
    ),
):
    deleted = await product_service.delete_product(
        product_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return {
        "message": "Product deleted successfully."
    }


# ======================================================
# Increase Stock
# ======================================================

@router.patch(
    "/{product_id}/stock/increase",
    response_model=ProductResponse,
)
async def increase_stock(
    product_id: int,
    request: StockUpdateRequest,
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        require_admin(),
    ),
):
    product = await product_service.increase_stock(
        product_id,
        request.quantity,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


# ======================================================
# Decrease Stock
# ======================================================

@router.patch(
    "/{product_id}/stock/decrease",
    response_model=ProductResponse,
)
async def decrease_stock(
    product_id: int,
    request: StockUpdateRequest,
    product_service: ProductService = Depends(
        get_product_service,
    ),
    current_user: User = Depends(
        require_admin(),
    ),
):
    try:
        product = await product_service.decrease_stock(
            product_id,
            request.quantity,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product