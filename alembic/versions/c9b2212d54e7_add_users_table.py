"""Add users table

Revision ID: c9b2212d54e7
Revises: e5a91d2e001d
Create Date: 2022-06-22 08:53:06.583981

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import PrimaryKeyConstraint


# revision identifiers, used by Alembic.
revision = 'c9b2212d54e7'
down_revision = 'e5a91d2e001d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
