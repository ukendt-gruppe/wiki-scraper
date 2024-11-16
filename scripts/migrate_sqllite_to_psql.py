import sqlite3
import psycopg2
from dotenv import load_dotenv
import os

def migrate_data():
    load_dotenv()

    # Connect to SQLite
    sqlite_conn = sqlite3.connect('migrations/whoknows.db')
    sqlite_cursor = sqlite_conn.cursor()

    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(os.getenv('LOCAL_DATABASE_URL'))
    pg_cursor = pg_conn.cursor()

    try:
        # Migrate wiki_articles
        sqlite_cursor.execute("SELECT * FROM wiki_articles")
        articles = sqlite_cursor.fetchall()
        
        for article in articles:
            pg_cursor.execute(
                """
                INSERT INTO wiki_articles (id, url, title, content, scraped_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE 
                SET url=EXCLUDED.url, title=EXCLUDED.title, 
                    content=EXCLUDED.content, scraped_at=EXCLUDED.scraped_at
                """,
                article
            )

        # Migrate users
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        for user in users:
            pg_cursor.execute(
                """
                INSERT INTO users (id, username, email, password)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE 
                SET username=EXCLUDED.username, email=EXCLUDED.email, 
                    password=EXCLUDED.password
                """,
                user
            )

        # Migrate pages
        sqlite_cursor.execute("SELECT * FROM pages")
        pages = sqlite_cursor.fetchall()
        
        for page in pages:
            pg_cursor.execute(
                """
                INSERT INTO pages (title, url, language, last_updated, content)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (title) DO UPDATE 
                SET url=EXCLUDED.url, language=EXCLUDED.language,
                    last_updated=EXCLUDED.last_updated, content=EXCLUDED.content
                """,
                page
            )

        pg_conn.commit()

    except Exception as e:
        pg_conn.rollback()
        raise e
    finally:
        sqlite_conn.close()
        pg_conn.close()

def test_connection():
    load_dotenv()
    try:
        conn = psycopg2.connect(os.getenv('LOCAL_DATABASE_URL'))
        print("Successfully connected to local PostgreSQL database!")
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    if test_connection():
        migrate_data()