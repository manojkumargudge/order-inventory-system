"""update order status enum

Revision ID: 7c8317bba42c
Revises: 8e5341931243
Create Date: 2026-07-02 11:51:41.099157

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c8317bba42c"
down_revision: Union[str, Sequence[str], None] = "8e5341931243"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


order_status_enum = sa.Enum(
    "PENDING",
    "CONFIRMED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    name="orderstatus",
)


def upgrade() -> None:
    """Upgrade schema."""

    # Create the PostgreSQL ENUM type
    order_status_enum.create(op.get_bind(), checkfirst=True)

    # Convert VARCHAR column to ENUM
    op.alter_column(
        "orders",
        "status",
        existing_type=sa.VARCHAR(length=20),
        type_=order_status_enum,
        existing_nullable=False,
        postgresql_using="status::orderstatus",
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Convert ENUM back to VARCHAR
    op.alter_column(
        "orders",
        "status",
        existing_type=order_status_enum,
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
        postgresql_using="status::text",
    )

    # Drop the ENUM type
    order_status_enum.drop(op.get_bind(), checkfirst=True)