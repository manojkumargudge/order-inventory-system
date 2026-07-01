from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product import Product
from src.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    """
    Repository for product database operations.
    """

    def __init__(self, db: AsyncSession):
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
            select(Product).where(Product.name == name)
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

        return result.scalars().all()

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
            setattr(product, key, value)

        await self.db.flush()

        await self.db.refresh(product)

        return product

    async def save(
        self,
        product: Product,
    ) -> Product:
        """
        Save changes to an existing product.
        """

        await self.db.flush()

        await self.db.refresh(product)

        return product

    async def delete_product(
        self,
        product: Product,
    ) -> None:
        """
        Delete a product.
        """

        await self.db.delete(product)

        await self.db.flush()