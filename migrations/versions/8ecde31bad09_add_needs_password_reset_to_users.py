"""add_needs_password_reset_to_users

Revision ID: 8ecde31bad09
Revises: 49926967c29c
Create Date: 2024-12-05 13:16:45.109550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ecde31bad09'
down_revision: Union[str, None] = '49926967c29c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
       op.add_column('users',
           sa.Column('needs_password_reset', sa.Boolean(), 
                     nullable=False, 
                     server_default='true')
       )

def downgrade() -> None:
       op.drop_column('users', 'needs_password_reset')
