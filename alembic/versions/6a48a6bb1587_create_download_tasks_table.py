"""Create download_tasks table

Revision ID: 6a48a6bb1587
Revises: 53dfc6100e78
Create Date: 2025-10-10 23:18:25.476386

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a48a6bb1587"
down_revision: Union[str, Sequence[str], None] = "53dfc6100e78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "download_tasks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("queue_task_id", sa.String(100), unique=True, nullable=True),
        sa.Column("episode_id", sa.String(64), index=True, nullable=True),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(50),
            index=True,
            nullable=False,
            comment="pending, processing, success, failed",
        ),
        sa.Column(
            "is_unread",
            sa.Boolean,
            index=True,
            nullable=True,
            default=sa.null(),
            comment="unread status",
        ),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, index=True, nullable=False),
        sa.Column("completed_at", sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
