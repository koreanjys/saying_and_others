"""add good, bad to saying

Revision ID: 8b0c169d176a
Revises: cbb20b4340d0
Create Date: 2024-03-08 18:13:33.828106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # 추가
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8b0c169d176a'
down_revision: Union[str, None] = 'cbb20b4340d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fourchar', 'contents_good',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('fourchar', 'contents_bad',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('saying', 'contents_good',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('saying', 'contents_bad',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('saying', 'contents_bad',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('saying', 'contents_good',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('fourchar', 'contents_bad',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('fourchar', 'contents_good',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###