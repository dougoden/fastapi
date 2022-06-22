"""Add column created_at to posts

Revision ID: 53ae0763c428
Revises: 9116e73c976e
Create Date: 2022-06-22 09:30:32.317075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53ae0763c428'
down_revision = '9116e73c976e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                     nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    pass
