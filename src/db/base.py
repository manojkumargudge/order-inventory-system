from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every model (User, Product, Order, Inventory, etc.)
    will inherit from this class.
    """

    pass