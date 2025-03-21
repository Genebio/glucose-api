"""Pytest configuration and fixtures."""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.infrastructure.database import Base
from app.main import get_application


@pytest.fixture(scope="session")
def test_db():
    """Create a test database."""
    # Use an in-memory SQLite database for tests
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Patch the get_db dependency
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    from app.infrastructure.database import get_db
    app = get_application()
    app.dependency_overrides[get_db] = override_get_db
    
    yield app
    
    # Clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create a test client."""
    with TestClient(test_db) as client:
        yield client