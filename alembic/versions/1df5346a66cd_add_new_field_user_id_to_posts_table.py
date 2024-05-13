"""add new field - user_id to posts table

Revision ID: 1df5346a66cd
Revises: 9ec588c00f7c
Create Date: 2024-05-12 14:00:42.084556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '1df5346a66cd'
down_revision: Union[str, None] = '9ec588c00f7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""
user_id = sa.Column(Integer, ForeignKey(sa.Column="users.id", ondelete="CASCADE"), nullable=False)
"""

TABLENAME: str = "posts"


def upgrade() -> None:
    op.add_column(TABLENAME,
                  sa.Column("user_id", sa.Integer, sa.ForeignKey(column="users.id", ondelete="CASCADE"),
                            nullable=False))


def downgrade() -> None:
    op.drop_column(TABLENAME, "user_id")
