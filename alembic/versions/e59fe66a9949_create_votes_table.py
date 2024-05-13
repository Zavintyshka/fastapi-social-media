"""create votes table

Revision ID: e59fe66a9949
Revises: 1df5346a66cd
Create Date: 2024-05-12 14:04:41.269249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e59fe66a9949'
down_revision: Union[str, None] = '1df5346a66cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""
user_id = Column(Integer, Foreign Key(column="users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
post_id = Column(Integer, ForeignKey(column="posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
"""

TABLENAME = "votes"


def upgrade() -> None:
    op.create_table(TABLENAME,
                    sa.Column("user_id", sa.Integer, sa.ForeignKey(column="users.id", ondelete="CASCADE"),
                              primary_key=True, nullable=False),
                    sa.Column("post_id", sa.Integer, sa.ForeignKey(column="posts.id", ondelete="CASCADE"),
                              primary_key=True, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table(TABLENAME)
