"""Adding new fields in posts table

Revision ID: 9f9cf1f78353
Revises: 4881989b9c48
Create Date: 2024-05-12 12:56:00.600043

"""
from typing import Sequence, Union

import sqlalchemy
from alembic import op
import sqlalchemy as sa

from app.api_types import Category

# revision identifiers, used by Alembic.
revision: str = '9f9cf1f78353'

down_revision: Union[str, None] = '4881989b9c48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""
    text = sa.Column(sa.String, nullable=False)
    category = sa.Column(Enum(Category), nullable=False)
    score = sa.Column(Integer, nullable=False)
    created_at = sa.Column(TIMESTAMP(timezone=True), server_default=func.now())
"""

TABLENAME: str = "posts"


def upgrade() -> None:
    op.execute("CREATE TYPE category as ENUM('simulator', 'rpg','action')")
    op.add_column(TABLENAME, sa.Column("text", sa.String, nullable=False))
    op.add_column(TABLENAME, sa.Column("category", sa.Enum(Category), nullable=False))
    op.add_column(TABLENAME, sa.Column("score", sa.Integer, nullable=False))
    op.add_column(TABLENAME, sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_column(TABLENAME, "text")
    op.drop_column(TABLENAME, "category")
    op.drop_column(TABLENAME, "score")
    op.drop_column(TABLENAME, "created_at")
    op.execute("DROP TYPE category")
