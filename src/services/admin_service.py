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