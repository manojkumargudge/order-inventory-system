from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import UserRole
from src.core.security import hash_password
from src.models.user import User
from src.schemas.auth import UserRegister


class UserRepository:
    """
    Repository for user database operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Get a user by ID.
        """
        return await self.db.get(User, user_id)

    async def get_by_username(self, username: str) -> User | None:
        """
        Get a user by username.
        """
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """
        Get a user by email.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserRegister) -> User:
        """
        Create a new user.
        """
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
            role=UserRole.CUSTOMER,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update_role(
        self,
        user: User,
        role: UserRole,
    ) -> User:
        """
        Update a user's role.
        """
        user.role = role

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user