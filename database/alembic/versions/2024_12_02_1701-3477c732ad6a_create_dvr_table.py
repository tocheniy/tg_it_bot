"""create dvr table

Revision ID: 3477c732ad6a
Revises: 
Create Date: 2024-12-02 17:01:24.890134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3477c732ad6a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dvrs',
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('ip', sa.String(length=16), nullable=False),
    sa.Column('login', sa.String(length=16), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dvrs')
    # ### end Alembic commands ###
