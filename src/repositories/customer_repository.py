from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.customer import Customer
from src.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:
    """
    Repository for Customer database operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_customer(
        self,
        user_id: int,
        customer_data: CustomerCreate,
    ) -> Customer:
        customer = Customer(
            user_id=user_id,
            **customer_data.model_dump(),
        )

        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)

        return customer

    async def get_customer_by_user_id(
        self,
        user_id: int,
    ) -> Customer | None:
        result = await self.db.execute(
            select(Customer).where(Customer.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def update_customer(
        self,
        customer: Customer,
        customer_data: CustomerUpdate,
    ) -> Customer:
        update_data = customer_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(customer, field, value)

        await self.db.commit()
        await self.db.refresh(customer)

        return customer

    async def delete_customer(
        self,
        customer: Customer,
    ) -> None:
        await self.db.delete(customer)
        await self.db.commit()