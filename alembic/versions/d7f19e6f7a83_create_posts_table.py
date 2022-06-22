"""Create Posts table

Revision ID: d7f19e6f7a83
Revises: 
Create Date: 2022-06-21 12:40:29.028563

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd7f19e6f7a83'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    # sa.Column('published', sa.Boolean(),
                    #           nullable=False, server_default='TRUE'),
                    # sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                    #           nullable=False, server_default=sa.text('NOW()'))
                    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
