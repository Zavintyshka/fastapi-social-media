"""create users table

Revision ID: 9ec588c00f7c
Revises: 9f9cf1f78353
Create Date: 2024-05-12 13:36:51.649690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.api_types import Gender

# revision identifiers, used by Alembic.
revision: str = '9ec588c00f7c'
down_revision: Union[str, None] = '9f9cf1f78353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""
id = Column(Integer, primary_key=True, nullable=False)
email = Column(String, unique=True, nullable=False)
password = Column(String, nullable=False)
firstname = Column(String, nullable=False)
lastname = Column(String, nullable=False)
age = Column(Integer, nullable=True)
gender = Column(Enum(Gender), nullable=True)
registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
"""

TABLENAME: str = "users"


def upgrade() -> None:
    op.create_table(TABLENAME,
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("email", sa.String, unique=True, nullable=False),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("firstname", sa.String, nullable=False),
                    sa.Column("lastname", sa.String, nullable=False),
                    sa.Column("age", sa.Integer, nullable=True),
                    sa.Column("gender", sa.Enum(Gender), nullable=False),
                    sa.Column("registered_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(),
                              nullable=False),
                    )


def downgrade() -> None:
    op.drop_table(TABLENAME)
    op.execute("DROP TYPE gender")
