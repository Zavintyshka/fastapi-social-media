"""create posts table

Revision ID: 4881989b9c48
Revises: 
Create Date: 2024-05-12 12:39:58.770731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4881989b9c48'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table("posts")

