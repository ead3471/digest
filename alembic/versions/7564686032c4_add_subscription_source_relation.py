"""add subscription - source relation

Revision ID: 7564686032c4
Revises: b9e1219f2c12
Create Date: 2023-07-23 11:49:27.610396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7564686032c4'
down_revision = 'b9e1219f2c12'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriptions', sa.Column('source_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'subscriptions', 'sources', ['source_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subscriptions', type_='foreignkey')
    op.drop_column('subscriptions', 'source_id')
    # ### end Alembic commands ###