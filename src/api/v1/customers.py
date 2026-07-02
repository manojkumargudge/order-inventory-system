from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.db.session import get_db
from src.models.user import User
from src.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from src.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)

    return await service.create_customer(
        current_user.id,
        customer_data,
    )


@router.get(
    "/me",
    response_model=CustomerResponse,
)
async def get_customer(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)

    return await service.get_customer(current_user.id)


@router.put(
    "/me",
    response_model=CustomerResponse,
)
async def update_customer(
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)

    return await service.update_customer(
        current_user.id,
        customer_data,
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customer(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CustomerService(db)

    await service.delete_customer(current_user.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)