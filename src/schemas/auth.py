from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.core.enums import UserRole


class UserRegister(BaseModel):
    """
    Schema for user registration.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
    )

    email: EmailStr

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
    )


class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """
    User information returned by the API.
    """

    id: int
    username: str
    email: EmailStr
    full_name: str
    is_active: bool
    is_superuser: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)