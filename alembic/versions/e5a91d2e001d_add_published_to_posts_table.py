"""Add published to posts table

Revision ID: e5a91d2e001d
Revises: d7f19e6f7a83
Create Date: 2022-06-21 13:12:18.540270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a91d2e001d'
down_revision = 'd7f19e6f7a83'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    pass
