"""Add production code to episode

Revision ID: c03e060df1b8
Revises: 928d4358646c
Create Date: 2023-12-21 20:12:27.108201
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c03e060df1b8"
down_revision: Union[str, None] = "928d4358646c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "episodes",
        sa.Column(
            "production_code",
            sa.VARCHAR(length=8),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "episodes",
        "production_code",
    )
