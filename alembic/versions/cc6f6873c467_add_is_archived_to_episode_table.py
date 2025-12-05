"""add is_archived to episode table

Revision ID: cc6f6873c467
Revises: 6a48a6bb1587
Create Date: 2025-12-05 15:03:49.929610

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc6f6873c467"
down_revision: Union[str, Sequence[str], None] = "6a48a6bb1587"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "episode",
        sa.Column(
            "is_archived", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("episode", "is_archived")
