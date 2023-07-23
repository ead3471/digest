"""change default value in created

Revision ID: 39203dc13bba
Revises: 78d2e4b21d3a
Create Date: 2023-07-23 00:53:21.528195

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '39203dc13bba'
down_revision = '78d2e4b21d3a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('digests', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('posts', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('digests', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###