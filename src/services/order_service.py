from decimal import Decimal

from src.core.enums import OrderStatus
from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.product import Product
from src.repositories.order_repository import OrderRepository
from src.repositories.product_repository import ProductRepository
from src.schemas.order import OrderCreate
from src.services.order_status_service import OrderStatusService


class OrderService:
    """
    Order business logic.
    """

    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository

    async def create_order(
        self,
        user_id: int,
        order_data: OrderCreate,
    ) -> Order:
        """
        Create a new order.
        """

        if not order_data.items:
            raise ValueError(
                "Order must contain at least one item."
            )

        try:

            total_amount = Decimal("0.00")

            requested_quantities: dict[int, int] = {}

            for item in order_data.items:
                requested_quantities[item.product_id] = (
                    requested_quantities.get(item.product_id, 0)
                    + item.quantity
                )

            products_by_id: dict[int, Product] = {}

            for product_id, quantity in requested_quantities.items():

                product = await self.product_repository.get_by_id(
                    product_id
                )

                if product is None:
                    raise ValueError(
                        f"Product with ID {product_id} does not exist."
                    )

                if not await self.product_repository.has_sufficient_stock(
                    product,
                    quantity,
                ):
                    raise ValueError(
                        f"Insufficient stock for product '{product.name}'."
                    )

                products_by_id[product_id] = product

            order = Order(
                user_id=user_id,
                total_amount=Decimal("0.00"),
                status=OrderStatus.PENDING,
            )

            order = await self.order_repository.create_order(
                order
            )

            for item in order_data.items:

                product = products_by_id[item.product_id]

                subtotal = product.price * item.quantity

                total_amount += subtotal

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.price,
                )

                await self.order_repository.create_order_item(
                    order_item
                )

                await self.product_repository.decrease_stock(
                    product,
                    item.quantity,
                )

            order.total_amount = total_amount

            order = await self.order_repository.save(
                order
            )

            await self.order_repository.db.commit()

            return await self.order_repository.get_order_by_id(
                order.id
            )

        except Exception:

            await self.order_repository.db.rollback()

            raise

    async def get_order_by_id(
        self,
        order_id: int,
        user_id: int,
    ) -> Order | None:
        """
        Get an order by its ID for the current user.
        """

        return await self.order_repository.get_order_by_id_and_user(
            order_id,
            user_id,
        )

    async def get_orders_by_user(
        self,
        user_id: int,
    ) -> list[Order]:
        """
        Get all orders belonging to a user.
        """

        return await self.order_repository.get_orders_by_user(
            user_id
        )

    async def cancel_order(
        self,
        order_id: int,
        user_id: int,
    ) -> Order | None:
        """
        Cancel an existing order and restore inventory.
        """

        order = await self.order_repository.get_order_by_id_and_user(
            order_id,
            user_id,
        )

        if order is None:
            return None

        if order.status != OrderStatus.PENDING:
            raise ValueError(
                "Only pending orders can be cancelled."
            )

        try:

            for item in order.order_items:

                product = await self.product_repository.get_by_id(
                    item.product_id
                )

                if product is not None:

                    await self.product_repository.increase_stock(
                        product,
                        item.quantity,
                    )

            order.status = OrderStatus.CANCELLED

            order = await self.order_repository.save(
                order
            )

            await self.order_repository.db.commit()

            return await self.order_repository.get_order_by_id(
                order.id
            )

        except Exception:

            await self.order_repository.db.rollback()

            raise

    async def update_order_status(
        self,
        order_id: int,
        user_id: int,
        new_status: OrderStatus,
    ) -> Order | None:
        """
        Update an order status after validating the workflow.
        """

        order = await self.order_repository.get_order_by_id_and_user(
            order_id,
            user_id,
        )

        if order is None:
            return None

        OrderStatusService.validate_transition(
            order.status,
            new_status,
        )

        order.status = new_status

        try:

            order = await self.order_repository.save(
                order
            )

            await self.order_repository.db.commit()

            return await self.order_repository.get_order_by_id(
                order.id
            )

        except Exception:

            await self.order_repository.db.rollback()

            raise