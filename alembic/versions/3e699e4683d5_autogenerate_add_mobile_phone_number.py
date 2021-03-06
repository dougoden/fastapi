"""Autogenerate - add mobile phone number

Revision ID: 3e699e4683d5
Revises: 3a47fc054404
Create Date: 2022-06-22 09:53:39.955763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e699e4683d5'
down_revision = '3a47fc054404'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_mobile', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_mobile')
    # ### end Alembic commands ###
