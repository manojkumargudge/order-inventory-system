from src.core.enums import UserRole
from src.repositories.admin_repository import AdminRepository


class AdminService:
    """
    Business logic for admin operations.
    """

    def __init__(
        self,
        admin_repository: AdminRepository,
    ):
        self.admin_repository = admin_repository

    async def get_all_orders(
        self,
    ):
        """
        Get all orders.
        """

        return await self.admin_repository.get_all_orders()

    async def get_order_by_id(
        self,
        order_id: int,
    ):
        """
        Get order by ID.
        """

        return await self.admin_repository.get_order_by_id(
            order_id
        )

    async def get_dashboard_stats(
        self,
    ):
        """
        Get admin dashboard statistics.
        """

        return await self.admin_repository.get_dashboard_stats()

    async def get_low_stock_products(
        self,
        threshold: int = 10,
    ):
        """
        Get products with low stock.
        """

        return await self.admin_repository.get_low_stock_products(
            threshold
        )

    async def get_out_of_stock_products(
        self,
    ):
        """
        Get products that are out of stock.
        """

        return await self.admin_repository.get_out_of_stock_products()

    async def restock_product(
        self,
        product_id: int,
        quantity: int,
    ):
        """
        Increase product stock.
        """

        return await self.admin_repository.restock_product(
            product_id,
            quantity,
        )

    async def change_user_role(
        self,
        current_user_id: int,
        target_user_id: int,
        role: UserRole,
    ):
        """
        Change a user's role.
        """

        if current_user_id == target_user_id:
            raise ValueError(
                "You cannot change your own role."
            )

        user = await self.admin_repository.get_user_by_id(
            target_user_id
        )

        if user is None:
            raise ValueError("User not found.")

        user.role = role

        return await self.admin_repository.update_user_role(
            user
        )