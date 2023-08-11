"""creating user table

Revision ID: 8f2897396f13
Revises: 772afd47e67d
Create Date: 2023-08-09 21:14:52.476623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f2897396f13'
down_revision: Union[str, None] = '7374b84bae52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255)),
        sa.Column('password_hash', sa.String(255)),
        sa.Column('email', sa.String(255)),
        sa.Column('role', sa.String(255)),
        sa.Column('is_active', sa.Boolean),
        sa.Column('created_at', sa.TIMESTAMP)
    )


def downgrade() -> None:
    op.drop_table('users')
