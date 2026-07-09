"""add user role

Revision ID: 2562fe7c89b6
Revises: 941adca729f7
Create Date: 2026-07-08 12:18:14.955141

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2562fe7c89b6"
down_revision: Union[str, Sequence[str], None] = "941adca729f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# PostgreSQL Enum
user_role_enum = sa.Enum(
    "ADMIN",
    "CUSTOMER",
    name="userrole",
)


def upgrade() -> None:
    """Upgrade schema."""

    # Create enum type
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # Add column
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            nullable=False,
            server_default="CUSTOMER",
        ),
    )

    # Remove default for future inserts
    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")

    # Drop enum type
    user_role_enum.drop(op.get_bind(), checkfirst=True)