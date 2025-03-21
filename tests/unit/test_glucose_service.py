"""Unit tests for glucose service."""
import unittest
from datetime import datetime
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.application.services.glucose_service import GlucoseService
from app.domain.models.glucose_level import GlucoseLevel
from app.domain.schemas.glucose_level import GlucoseLevelCreate


class TestGlucoseService:
    """Tests for GlucoseService."""
    
    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        repository = AsyncMock()
        repository.get_by_id = AsyncMock()
        repository.get_by_user_id = AsyncMock()
        repository.create = AsyncMock()
        repository.create_many = AsyncMock()
        repository.update = AsyncMock()
        repository.delete = AsyncMock()
        return repository
    
    @pytest.fixture
    def service(self, mock_repository):
        """Create the service with a mock repository."""
        return GlucoseService(mock_repository)
    
    @pytest.fixture
    def sample_glucose_level(self):
        """Create a sample glucose level."""
        return GlucoseLevel(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            timestamp=datetime.utcnow(),
            glucose_value=120.5,
            device_type="Test Device",
            device_id="TEST-123",
            record_type="0",
            notes=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    @pytest.mark.asyncio
    async def test_get_glucose_level(self, service, mock_repository, sample_glucose_level):
        """Test get_glucose_level method."""
        # Set up mock
        mock_repository.get_by_id.return_value = sample_glucose_level
        
        # Call service
        result = await service.get_glucose_level(sample_glucose_level.id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(sample_glucose_level.id)
        assert result == sample_glucose_level
    
    @pytest.mark.asyncio
    async def test_get_glucose_levels(self, service, mock_repository, sample_glucose_level):
        """Test get_glucose_levels method."""
        # Set up mock
        mock_repository.get_by_user_id.return_value = ([sample_glucose_level], 1)
        
        # Call service
        result = await service.get_glucose_levels(
            sample_glucose_level.user_id,
            start_time=None,
            end_time=None,
            page=1,
            page_size=10,
            sort_by="timestamp",
            sort_order="desc"
        )
        
        # Assert
        mock_repository.get_by_user_id.assert_called_once_with(
            sample_glucose_level.user_id,
            None, None, 1, 10, "timestamp", "desc"
        )
        assert result.items == [sample_glucose_level]
        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 10
        assert result.total_pages == 1
    
    @pytest.mark.asyncio
    async def test_create_glucose_level(self, service, mock_repository, sample_glucose_level):
        """Test create_glucose_level method."""
        # Set up mock
        mock_repository.create.return_value = sample_glucose_level
        
        # Create data
        glucose_data = GlucoseLevelCreate(
            user_id=sample_glucose_level.user_id,
            timestamp=sample_glucose_level.timestamp,
            glucose_value=sample_glucose_level.glucose_value,
            device_type=sample_glucose_level.device_type,
            device_id=sample_glucose_level.device_id,
            record_type=sample_glucose_level.record_type,
            notes=sample_glucose_level.notes
        )
        
        # Call service
        with patch('uuid.uuid4', return_value=sample_glucose_level.id):
            result = await service.create_glucose_level(glucose_data)
        
        # Assert
        assert mock_repository.create.called
        assert result == sample_glucose_level