"""Add foreign-key to posts table

Revision ID: 9116e73c976e
Revises: c9b2212d54e7
Create Date: 2022-06-22 09:17:44.082362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9116e73c976e'
down_revision = 'c9b2212d54e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_owner_id_fkey', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_owner_id_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
