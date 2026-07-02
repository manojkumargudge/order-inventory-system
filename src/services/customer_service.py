from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.customer import Customer
from src.repositories.customer_repository import CustomerRepository
from src.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """
    Service layer for Customer business logic.
    """

    def __init__(self, db: AsyncSession):
        self.repository = CustomerRepository(db)

    async def create_customer(
        self,
        user_id: int,
        customer_data: CustomerCreate,
    ) -> Customer:
        existing_customer = await self.repository.get_customer_by_user_id(
            user_id
        )

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer profile already exists.",
            )

        return await self.repository.create_customer(
            user_id,
            customer_data,
        )

    async def get_customer(
        self,
        user_id: int,
    ) -> Customer:
        customer = await self.repository.get_customer_by_user_id(user_id)

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer profile not found.",
            )

        return customer

    async def update_customer(
        self,
        user_id: int,
        customer_data: CustomerUpdate,
    ) -> Customer:
        customer = await self.get_customer(user_id)

        return await self.repository.update_customer(
            customer,
            customer_data,
        )

    async def delete_customer(
        self,
        user_id: int,
    ) -> None:
        customer = await self.get_customer(user_id)

        await self.repository.delete_customer(customer)