from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enums import UserRole
from src.core.security import decode_access_token
from src.db.session import get_db
from src.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns the currently authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise credentials_exception

    repository = UserRepository(db)

    user = await repository.get_by_username(username)

    if user is None:
        raise credentials_exception

    return user


def require_roles(*allowed_roles: UserRole):
    """
    Dependency to restrict endpoint access based on user roles.
    """

    async def role_checker(
        current_user=Depends(get_current_user),
    ):
        print("\n========== RBAC DEBUG ==========")
        print(f"Username      : {current_user.username}")
        print(f"Role          : {current_user.role}")
        print(f"Allowed Roles : {allowed_roles}")
        print(f"Role Type     : {type(current_user.role)}")
        print("================================\n")

        if current_user.role not in allowed_roles:
            print("❌ ACCESS DENIED")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        print("✅ ACCESS GRANTED")
        return current_user

    return role_checker


def require_admin():
    """
    Allow only ADMIN users.
    """
    return require_roles(UserRole.ADMIN)


def require_customer():
    """
    Allow only CUSTOMER users.
    """
    return require_roles(UserRole.CUSTOMER)