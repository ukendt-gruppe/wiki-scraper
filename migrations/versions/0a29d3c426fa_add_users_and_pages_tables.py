"""add_users_and_pages_tables

Revision ID: 0a29d3c426fa
Revises: 49926967c29c
Create Date: 2024-11-16 19:24:26.092578

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '0a29d3c426fa'
down_revision: Union[str, None] = '49926967c29c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False)
    )

    # Create pages table
    op.create_table(
        'pages',
        sa.Column('title', sa.String(length=500), primary_key=True),
        sa.Column('url', sa.String(length=500), nullable=False, unique=True),
        sa.Column('language', sa.String(length=2), nullable=False, server_default='en'),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.CheckConstraint("language IN ('en', 'da')")
    )

    # Insert default admin user
    op.execute(
        """
        INSERT INTO users (username, email, password) 
        VALUES ('admin', 'keamonk1@stud.kea.dk', '5f4dcc3b5aa765d61d8327deb882cf99')
        """
    )

def downgrade() -> None:
    op.drop_table('pages')
    op.drop_table('users')
