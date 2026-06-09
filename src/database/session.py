"""Database session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger
from src.config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session for dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    logger.info("Initializing database...")
    from src.database.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")


def drop_db():
    """Drop all tables (use with caution)"""
    logger.warning("Dropping all database tables...")
    from src.database.models import Base
    Base.metadata.drop_all(bind=engine)
    logger.info("Database dropped")
