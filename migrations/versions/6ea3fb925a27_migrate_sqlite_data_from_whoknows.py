"""migrate_sqlite_data_from_whoknows

Revision ID: 6ea3fb925a27
Revises: 0a29d3c426fa
Create Date: 2024-11-16 19:45:26.092578
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlite3
from datetime import datetime
from contextlib import closing
import os

# revision identifiers, used by Alembic.
revision: str = '6ea3fb925a27'
down_revision: Union[str, None] = '0a29d3c426fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Get the path in the migrations directory
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'whoknows.db')
    
    if not os.path.exists(db_path):
        print(f"SQLite database file not found at: {db_path}")
        return

    try:
        with closing(sqlite3.connect(db_path)) as sqlite_conn:
            sqlite_cursor = sqlite_conn.cursor()
            connection = op.get_bind()
            
            print("Connected to production database, starting migration...")
            
            # Migrate users table
            sqlite_cursor.execute('SELECT username, email, password FROM users')
            users = sqlite_cursor.fetchall()
            
            for user in users:
                if user[0] != 'admin':
                    try:
                        connection.execute(
                            sa.text('INSERT INTO users (username, email, password) VALUES (:username, :email, :password)'),
                            {"username": user[0], "email": user[1], "password": user[2]}
                        )
                    except Exception as e:
                        print(f"Error inserting user {user[0]}: {str(e)}")
                        continue

            # Migrate pages table
            sqlite_cursor.execute('SELECT title, url, language, last_updated, content FROM pages')
            pages = sqlite_cursor.fetchall()
            
            for page in pages:
                try:
                    connection.execute(
                        sa.text('INSERT INTO pages (title, url, language, last_updated, content) VALUES (:title, :url, :language, :last_updated, :content)'),
                        {
                            "title": page[0],
                            "url": page[1],
                            "language": page[2],
                            "last_updated": page[3] if page[3] else None,
                            "content": page[4]
                        }
                    )
                except Exception as e:
                    print(f"Error inserting page {page[0]}: {str(e)}")
                    continue

            # Migrate wiki_articles table
            sqlite_cursor.execute('SELECT id, url, title, content, scraped_at FROM wiki_articles')
            articles = sqlite_cursor.fetchall()
            
            for article in articles:
                try:
                    connection.execute(
                        sa.text('INSERT INTO wiki_articles (id, url, title, content, scraped_at) VALUES (:id, :url, :title, :content, :scraped_at)'),
                        {
                            "id": article[0],
                            "url": article[1],
                            "title": article[2],
                            "content": article[3],
                            "scraped_at": article[4] if article[4] else None
                        }
                    )
                except Exception as e:
                    print(f"Error inserting article {article[2]}: {str(e)}")
                    continue

            # Migrate migration_tracking table
            sqlite_cursor.execute('SELECT id, article_id, migrated_at, status, error_message FROM migration_tracking')
            tracking_records = sqlite_cursor.fetchall()
            
            for record in tracking_records:
                try:
                    connection.execute(
                        sa.text('INSERT INTO migration_tracking (id, article_id, migrated_at, status, error_message) VALUES (:id, :article_id, :migrated_at, :status, :error_message)'),
                        {
                            "id": record[0],
                            "article_id": record[1],
                            "migrated_at": record[2] if record[2] else None,
                            "status": record[3],
                            "error_message": record[4]
                        }
                    )
                except Exception as e:
                    print(f"Error inserting tracking record {record[0]}: {str(e)}")
                    continue

    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise

def downgrade() -> None:
    pass