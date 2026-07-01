from src.models.product import Product
from src.repositories.product_repository import ProductRepository
from src.schemas.product import ProductCreate, ProductUpdate


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

    async def get_all_products(
        self,
    ) -> list[Product]:
        """
        Get all products.
        """

        return await self.repository.get_all()

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