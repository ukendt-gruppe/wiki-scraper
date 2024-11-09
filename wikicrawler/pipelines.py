# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from .models import Base, WikiArticle
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
import os
import logging



class PostgresPipeline:
    def __init__(self):
        try:
            # Database connection parameters
            DB_USER = os.getenv('DB_USER', 'wiki_user')
            DB_PASSWORD = os.getenv('DB_PASSWORD', 'wiki_password')
            DB_HOST = os.getenv('DB_HOST', 'localhost')
            DB_PORT = os.getenv('DB_PORT', '5432')
            DB_NAME = os.getenv('DB_NAME', 'wiki_scraper')

            # Create database URL
            DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            
            # Initialize engine and session
            self.engine = create_engine(DATABASE_URL)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            
            logging.info("Database connection established successfully")
        except Exception as e:
            logging.error(f"Failed to initialize database connection: {str(e)}")
            self.engine = None
            self.session = None
            raise

    def process_item(self, item, spider):
        if not self.session:
            raise Exception("Database session not initialized")

        try:
            logging.info(f"Saving data for: {item['title']}")
            
            # Create the insert statement
            stmt = insert(WikiArticle).values(
                title=item['title'],
                content=item['content'],
                url=item['url'],
                scraped_at=item['scraped_at']
            )
            
            # Execute the statement
            self.session.execute(stmt)
            self.session.commit()
            
            return item
        except Exception as e:
            logging.error(f"Error saving to database: {str(e)}")
            if self.session:
                self.session.rollback()
            raise

    def close_spider(self, spider):
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()