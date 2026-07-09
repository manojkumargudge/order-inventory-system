from pydantic import BaseModel

from src.core.enums import UserRole


class UserRoleUpdate(BaseModel):
    """
    Schema for updating a user's role.
    """

    role: UserRole