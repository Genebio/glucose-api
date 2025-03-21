"""Unit tests for API endpoints."""
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_glucose_service():
    """Create a mock glucose service."""
    with patch('app.interfaces.api.v1.glucose_levels.SQLAlchemyGlucoseRepository') as mock_repo:
        with patch('app.interfaces.api.v1.glucose_levels.GlucoseService') as mock_service_cls:
            mock_service = AsyncMock()
            mock_service_cls.return_value = mock_service
            yield mock_service


def test_get_glucose_level(client, mock_glucose_service):
    """Test get_glucose_level endpoint."""
    # Setup
    glucose_id = str(uuid.uuid4())
    mock_glucose_service.get_glucose_level.return_value = {
        "id": glucose_id,
        "user_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "glucose_value": 120.5,
        "device_type": "Test Device",
        "device_id": "TEST-123",
        "record_type": "0",
        "notes": None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    # Execute
    response = client.get(f"/api/v1/levels/{glucose_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == glucose_id