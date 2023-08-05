"""create tables

Revision ID: 7374b84bae52
Revises: 
Create Date: 2023-08-05 15:07:29.965930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7374b84bae52'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('company_name', sa.String(255)),
        sa.Column('street', sa.String(255)),
        sa.Column('city', sa.String(255)),
        sa.Column('postal_code', sa.String(255)),
        sa.Column('state', sa.String(255)),
        sa.Column('country', sa.String(255)),
    )
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('first_name', sa.String(255)),
        sa.Column('last_name', sa.String(255)),
        sa.Column('position', sa.String(255)),
        sa.Column('age', sa.Integer),
        sa.Column('employment_tenure', sa.String(255)),
        sa.Column('department', sa.String(255)),
        sa.Column('salary', sa.Numeric(precision=6, scale=2)),
        sa.Column('performance_rating', sa.JSON),
        sa.Column('company_id', sa.Integer),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
    )


def downgrade() -> None:
    op.drop_table('employees')
    op.drop_table('companies')
