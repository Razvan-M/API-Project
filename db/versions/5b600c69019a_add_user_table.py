"""add user table

Revision ID: 5b600c69019a
Revises: 5a9da50cf1e6
Create Date: 2024-01-16 18:39:02.825038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b600c69019a'
down_revision: Union[str, None] = '5a9da50cf1e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
