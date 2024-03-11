"""edit created_url length

Revision ID: 61883fee5e85
Revises: 8b0c169d176a
Create Date: 2024-03-11 13:07:54.266824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # 추가
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '61883fee5e85'
down_revision: Union[str, None] = '8b0c169d176a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('createimage', 'created_url',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=500),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('createimage', 'created_url',
               existing_type=sa.String(length=500),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###
