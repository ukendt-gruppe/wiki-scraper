from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WikiArticle(Base):
    __tablename__ = 'wiki_articles'

    id = Column(Integer, primary_key=True)
    url = Column(String(500), unique=True)
    title = Column(String(500))
    content = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)

class MigrationTracking(Base):
    __tablename__ = 'migration_tracking'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('wiki_articles.id'))
    migrated_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))  # 'pending', 'completed', 'failed'
    error_message = Column(Text, nullable=True)