from src.core.security import (
    create_access_token,
    verify_password,
)
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.auth import UserRegister


class AuthService:
    """
    Authentication business logic.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, user_data: UserRegister) -> User:
        """
        Register a new user.
        """

        existing_username = await self.repository.get_by_username(
            user_data.username
        )

        if existing_username:
            raise ValueError("Username already exists.")

        existing_email = await self.repository.get_by_email(
            user_data.email
        )

        if existing_email:
            raise ValueError("Email already exists.")

        return await self.repository.create_user(user_data)

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> User | None:
        """
        Authenticate a user's credentials.
        """

        user = await self.repository.get_by_username(username)

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

    def create_token(self, user: User) -> str:
        """
        Generate a JWT access token.
        """

        return create_access_token(
            subject=user.username,
            role=user.role.value,
        )