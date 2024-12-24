"""change city table

Revision ID: 64a2e4693f1a
Revises: e3e58551c662
Create Date: 2024-12-24 11:04:55.820143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '64a2e4693f1a'
down_revision: Union[str, None] = 'e3e58551c662'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('short_name', sa.String(length=30), nullable=False))
    op.add_column('cities', sa.Column('ru_name', sa.String(length=30), nullable=False))
    op.drop_column('cities', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('name', mysql.VARCHAR(length=30), nullable=False))
    op.drop_column('cities', 'ru_name')
    op.drop_column('cities', 'short_name')
    # ### end Alembic commands ###