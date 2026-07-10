from pydantic import BaseModel, Field


class StockUpdateRequest(BaseModel):
    quantity: int = Field(
        ...,
        gt=0,
        description="Quantity to add or remove.",
    )