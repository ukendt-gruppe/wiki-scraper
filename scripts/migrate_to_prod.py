import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wikicrawler.models import WikiArticle, MigrationTracking
from dotenv import load_dotenv

load_dotenv()

def migrate_data():
    # Source (local) DB
    local_engine = create_engine(os.getenv('LOCAL_DATABASE_URL'))
    LocalSession = sessionmaker(bind=local_engine)
    local_session = LocalSession()

    # Target (production) DB
    prod_engine = create_engine(os.getenv('DATABASE_URL'))
    ProdSession = sessionmaker(bind=prod_engine)
    prod_session = ProdSession()

    try:
        # Get all articles from local DB
        local_articles = local_session.query(WikiArticle).all()
        
        for article in local_articles:
            # Check if article already exists in prod
            exists = prod_session.query(WikiArticle).filter_by(url=article.url).first()
            if not exists:
                # Create new article in prod
                new_article = WikiArticle(
                    url=article.url,
                    title=article.title,
                    content=article.content,
                    scraped_at=article.scraped_at
                )
                prod_session.add(new_article)
                prod_session.flush()  # Get the new ID

                # Track the migration
                tracking = MigrationTracking(
                    article_id=new_article.id,
                    status='completed'
                )
                prod_session.add(tracking)

        prod_session.commit()
        print("Migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        prod_session.rollback()
    finally:
        local_session.close()
        prod_session.close()

if __name__ == "__main__":
    migrate_data() 