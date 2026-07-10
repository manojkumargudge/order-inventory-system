from decimal import Decimal

from src.core.enums import (
    ProductSortField,
    SortOrder,
)
from src.models.product import Product
from src.repositories.product_repository import ProductRepository
from src.schemas.product import (
    ProductCreate,
    ProductUpdate,
)


class ProductService:
    """
    Product business logic.
    """

    def __init__(
        self,
        repository: ProductRepository,
    ):
        self.repository = repository

    async def create_product(
        self,
        product_data: ProductCreate,
    ) -> Product:
        """
        Create a new product.
        """

        existing_product = await self.repository.get_by_name(
            product_data.name
        )

        if existing_product:
            raise ValueError(
                "Product with this name already exists."
            )

        try:
            product = await self.repository.create_product(
                product_data
            )

            await self.repository.db.commit()

            return product

        except Exception:
            await self.repository.db.rollback()
            raise

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

        return await self.repository.get_products(
            search=search,
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock,
            sort_by=sort_by,
            order=order,
            page=page,
            page_size=page_size,
        )

    async def get_product_by_id(
        self,
        product_id: int,
    ) -> Product | None:
        """
        Get product by ID.
        """

        return await self.repository.get_by_id(
            product_id
        )

    async def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate,
    ) -> Product | None:
        """
        Update an existing product.
        """

        product = await self.repository.get_by_id(
            product_id
        )

        if product is None:
            return None

        try:
            updated_product = await self.repository.update_product(
                product,
                product_data,
            )

            await self.repository.db.commit()

            return updated_product

        except Exception:
            await self.repository.db.rollback()
            raise

    async def delete_product(
        self,
        product_id: int,
    ) -> bool:
        """
        Delete a product.
        """

        product = await self.repository.get_by_id(
            product_id
        )

        if product is None:
            return False

        try:
            await self.repository.delete_product(
                product
            )

            await self.repository.db.commit()

            return True

        except Exception:
            await self.repository.db.rollback()
            raise

    async def increase_stock(
        self,
        product_id: int,
        quantity: int,
    ) -> Product | None:
        """
        Increase product stock.
        """

        product = await self.repository.get_by_id(
            product_id
        )

        if product is None:
            return None

        try:
            updated_product = await self.repository.increase_stock(
                product,
                quantity,
            )

            await self.repository.db.commit()

            return updated_product

        except Exception:
            await self.repository.db.rollback()
            raise

    async def decrease_stock(
        self,
        product_id: int,
        quantity: int,
    ) -> Product | None:
        """
        Decrease product stock.
        """

        product = await self.repository.get_by_id(
            product_id
        )

        if product is None:
            return None

        if not await self.repository.has_sufficient_stock(
            product,
            quantity,
        ):
            raise ValueError(
                "Insufficient stock."
            )

        try:
            updated_product = await self.repository.decrease_stock(
                product,
                quantity,
            )

            await self.repository.db.commit()

            return updated_product

        except Exception:
            await self.repository.db.rollback()
            raise

    async def get_low_stock_products(
        self,
        threshold: int = 10,
    ) -> list[Product]:
        """
        Get products below the stock threshold.
        """

        return await self.repository.get_low_stock_products(
            threshold
        )

    async def get_out_of_stock_products(
        self,
    ) -> list[Product]:
        """
        Get products with zero stock.
        """

        return await self.repository.get_out_of_stock_products()