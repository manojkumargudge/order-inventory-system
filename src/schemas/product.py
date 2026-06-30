from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Product name",
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Product description",
    )

    price: float = Field(
        ...,
        gt=0,
        description="Product price",
    )

    stock: int = Field(
        default=0,
        ge=0,
        description="Available stock quantity",
    )


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    price: float | None = Field(
        default=None,
        gt=0,
    )

    stock: int | None = Field(
        default=None,
        ge=0,
    )


class ProductResponse(BaseModel):
    """
    Product information returned by the API.
    """

    id: int
    name: str
    description: str | None
    price: float
    stock: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)