"""add isnew field to pixa model

Revision ID: beac1f52e511
Revises: cb06f2e80882
Create Date: 2024-03-07 18:28:00.185104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # 추가


# revision identifiers, used by Alembic.
revision: str = 'beac1f52e511'
down_revision: Union[str, None] = 'cb06f2e80882'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pixabaydata', sa.Column('isnew', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pixabaydata', 'isnew')
    # ### end Alembic commands ###
