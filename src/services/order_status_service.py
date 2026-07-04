from src.models.enums import OrderStatus


class OrderStatusService:
    """
    Handles order status transitions.
    """

    VALID_TRANSITIONS = {
        OrderStatus.PENDING: {
            OrderStatus.CONFIRMED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.CONFIRMED: {
            OrderStatus.SHIPPED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.SHIPPED: {
            OrderStatus.DELIVERED,
        },
        OrderStatus.DELIVERED: set(),
        OrderStatus.CANCELLED: set(),
    }

    @classmethod
    def can_transition(
        cls,
        current_status: OrderStatus,
        new_status: OrderStatus,
    ) -> bool:
        """
        Returns True if the transition is allowed.
        """
        return new_status in cls.VALID_TRANSITIONS.get(
            current_status,
            set(),
        )

    @classmethod
    def validate_transition(
        cls,
        current_status: OrderStatus,
        new_status: OrderStatus,
    ) -> None:
        """
        Raises ValueError if transition is invalid.
        """
        if not cls.can_transition(current_status, new_status):
            raise ValueError(
                f"Invalid status transition: "
                f"{current_status.value} → {new_status.value}"
            )