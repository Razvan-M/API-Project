"""add content column to posts table

Revision ID: 5a9da50cf1e6
Revises: 6a775e04d506
Create Date: 2024-01-16 18:15:35.563347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a9da50cf1e6'
down_revision: Union[str, None] = '6a775e04d506'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
