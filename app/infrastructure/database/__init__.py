"""Database module."""
from app.infrastructure.database.connection import engine, get_db, Base, SessionLocal
from app.infrastructure.database.models import GlucoseLevel

# Create all tables by importing models and then calling create_all
Base.metadata.create_all(bind=engine)

__all__ = ["engine", "get_db", "Base", "GlucoseLevel", "SessionLocal"]