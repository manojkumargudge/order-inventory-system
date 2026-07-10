from decimal import Decimal

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.core.enums import (
    ProductSortField,
    SortOrder,
)
from src.models.product import Product
from src.schemas.product import (
    ProductCreate,
    ProductUpdate,
)


class ProductRepository:
    """
    Repository for product database operations.
    """

    SORT_FIELD_MAPPING = {
        ProductSortField.NAME: Product.name,
        ProductSortField.PRICE: Product.price,
        ProductSortField.STOCK: Product.stock,
        ProductSortField.CREATED_AT: Product.created_at,
    }

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create_product(
        self,
        product_data: ProductCreate,
    ) -> Product:
        """
        Create a new product.
        """

        product = Product(
            **product_data.model_dump()
        )

        self.db.add(product)

        await self.db.flush()
        await self.db.refresh(product)

        return product

    async def get_by_id(
        self,
        product_id: int,
    ) -> Product | None:
        """
        Get product by ID.
        """

        return await self.db.get(
            Product,
            product_id,
        )

    async def get_by_name(
        self,
        name: str,
    ) -> Product | None:
        """
        Get product by name.
        """

        result = await self.db.execute(
            select(Product).where(
                Product.name == name
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
    ) -> list[Product]:
        """
        Get all products.
        """

        result = await self.db.execute(
            select(Product)
        )

        return list(result.scalars().all())

    async def get_products(
        self,
        search: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        in_stock: bool | None = None,
        sort_by: ProductSortField | None = None,
        order: SortOrder = SortOrder.ASC,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Product]:
        """
        Fetch products with search,
        filtering,
        sorting,
        and pagination.
        """

        query = select(Product)

        query = self._apply_search(
            query,
            search,
        )

        query = self._apply_filters(
            query,
            min_price,
            max_price,
            in_stock,
        )

        query = self._apply_sorting(
            query,
            sort_by,
            order,
        )

        query = self._apply_pagination(
            query,
            page,
            page_size,
        )

        result = await self.db.execute(
            query
        )

        return list(
            result.scalars().all()
        )

    def _apply_search(
        self,
        query: Select,
        search: str | None,
    ) -> Select:
        """
        Apply search conditions.
        """

        if not search:
            return query

        search_term = f"%{search}%"

        return query.where(
            or_(
                Product.name.ilike(
                    search_term
                ),
                Product.description.ilike(
                    search_term
                ),
            )
        )

    def _apply_filters(
        self,
        query: Select,
        min_price: Decimal | None,
        max_price: Decimal | None,
        in_stock: bool | None,
    ) -> Select:
        """
        Apply filter conditions.
        """

        if min_price is not None:
            query = query.where(
                Product.price >= min_price
            )

        if max_price is not None:
            query = query.where(
                Product.price <= max_price
            )

        if in_stock is True:
            query = query.where(
                Product.stock > 0
            )

        return query

    def _apply_sorting(
        self,
        query: Select,
        sort_by: ProductSortField | None,
        order: SortOrder,
    ) -> Select:
        """
        Apply sorting.
        """

        if sort_by is None:
            return query

        column = self.SORT_FIELD_MAPPING.get(
            sort_by
        )

        if column is None:
            return query

        if order == SortOrder.DESC:
            return query.order_by(
                column.desc()
            )

        return query.order_by(
            column.asc()
        )

    def _apply_pagination(
        self,
        query: Select,
        page: int,
        page_size: int,
    ) -> Select:
        """
        Apply pagination.
        """

        offset = (
            page - 1
        ) * page_size

        return query.offset(
            offset
        ).limit(
            page_size
        )

    async def update_product(
        self,
        product: Product,
        product_data: ProductUpdate,
    ) -> Product:
        """
        Update an existing product.
        """

        update_data = product_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                product,
                key,
                value,
            )

        await self.db.flush()
        await self.db.refresh(
            product
        )

        return product

    async def save(
        self,
        product: Product,
    ) -> Product:
        """
        Save changes to an existing product.
        """

        await self.db.flush()
        await self.db.refresh(
            product
        )

        return product

    async def delete_product(
        self,
        product: Product,
    ) -> None:
        """
        Delete a product.
        """

        await self.db.delete(
            product
        )

        await self.db.flush()

    # ======================================================
    # Inventory Management Methods
    # ======================================================

    async def has_sufficient_stock(
        self,
        product: Product,
        quantity: int,
    ) -> bool:
        """
        Check whether the requested
        quantity is available.
        """

        return (
            product.stock
            >= quantity
        )

    async def decrease_stock(
        self,
        product: Product,
        quantity: int,
    ) -> Product:
        """
        Reduce product stock.
        """

        product.stock -= quantity

        await self.db.flush()
        await self.db.refresh(
            product
        )

        return product

    async def increase_stock(
        self,
        product: Product,
        quantity: int,
    ) -> Product:
        """
        Increase product stock.
        """

        product.stock += quantity

        await self.db.flush()
        await self.db.refresh(
            product
        )

        return product

    async def get_low_stock_products(
        self,
        threshold: int = 10,
    ) -> list[Product]:
        """
        Fetch products whose stock
        is below the threshold.
        """

        result = await self.db.execute(
            select(Product).where(
                Product.stock <= threshold
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_out_of_stock_products(
        self,
    ) -> list[Product]:
        """
        Fetch products with zero stock.
        """

        result = await self.db.execute(
            select(Product).where(
                Product.stock == 0
            )
        )

        return list(
            result.scalars().all()
        )