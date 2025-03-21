"""Tests for import and export functionality."""
import io
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pandas as pd
import pytest

from app.application.services.glucose_service import GlucoseService
from app.domain.models.glucose_level import GlucoseLevel


class TestImportExport:
    """Tests for import and export functions."""
    
    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        repository = AsyncMock()
        repository.create_many = AsyncMock(return_value=[])
        repository.get_by_user_id = AsyncMock(return_value=([], 0))
        return repository
    
    @pytest.fixture
    def sample_csv_content(self):
        """Create sample CSV content."""
        return """Glukose-Werte,Erstellt am,25-02-2021 17:28 UTC,Erstellt von,aaa

Gerät,Seriennummer,Gerätezeitstempel,Aufzeichnungstyp,Glukosewert-Verlauf mg/dL,Glukose-Scan mg/dL,Nicht numerisches schnellwirkendes Insulin,Schnellwirkendes Insulin (Einheiten),Nicht numerische Nahrungsdaten,Kohlenhydrate (Gramm),Kohlenhydrate (Portionen),Nicht numerisches Depotinsulin,Depotinsulin (Einheiten),Notizen,Glukose-Teststreifen mg/dL,Keton mmol/L,Mahlzeiteninsulin (Einheiten),Korrekturinsulin (Einheiten),Insulin-Änderung durch Anwender (Einheiten)
FreeStyle LibreLink,1D48A10E-DDFB-4888-8158-026F08814832,18-02-2021 10:57,0,77,,,,,,,,,,,,,,
FreeStyle LibreLink,1D48A10E-DDFB-4888-8158-026F08814832,18-02-2021 11:12,0,78,,,,,,,,,,,,,,"""
    
    @pytest.fixture
    def sample_csv_file(self, sample_csv_content, tmp_path):
        """Create a sample CSV file."""
        file_path = tmp_path / "test_data.csv"
        with open(file_path, "w") as f:
            f.write(sample_csv_content)
        return file_path
    
    @pytest.mark.asyncio
    async def test_import_from_csv(self, mock_repository, sample_csv_file):
        """Test importing data from CSV."""
        # Setup
        service = GlucoseService(mock_repository)
        user_id = uuid.uuid4()
        
        # Execute
        with patch('uuid.uuid4', return_value=uuid.uuid4()):
            result = await service.import_from_csv(sample_csv_file, user_id)
        
        # Assert
        assert mock_repository.create_many.called
        assert result == 2  # Two valid rows in the sample CSV
    
    @pytest.mark.asyncio
    async def test_export_to_csv(self, mock_repository):
        """Test exporting data to CSV."""
        # Setup
        service = GlucoseService(mock_repository)
        user_id = uuid.uuid4()
        
        # Create sample data
        glucose_levels = [
            GlucoseLevel(
                id=uuid.uuid4(),
                user_id=user_id,
                timestamp=datetime.fromisoformat("2021-02-18T10:57:00"),
                glucose_value=77,
                device_type="FreeStyle LibreLink",
                device_id="1D48A10E-DDFB-4888-8158-026F08814832",
                record_type="0",
                notes=None
            )
        ]
        
        # Configure mock
        mock_repository.get_by_user_id.return_value = (glucose_levels, len(glucose_levels))
        
        # Execute
        result = await service.export_to_csv(user_id)
        
        # Assert
        assert "ID,User ID,Timestamp,Glucose Value (mg/dL)" in result
        assert "77" in result  # Check if glucose value is in the CSV
        
    @pytest.mark.asyncio
    async def test_export_to_json(self, mock_repository):
        """Test exporting data to JSON."""
        # Setup
        service = GlucoseService(mock_repository)
        user_id = uuid.uuid4()
        glucose_id = uuid.uuid4()
        
        # Create sample data
        glucose_levels = [
            GlucoseLevel(
                id=glucose_id,
                user_id=user_id,
                timestamp=datetime.fromisoformat("2021-02-18T10:57:00"),
                glucose_value=77,
                device_type="FreeStyle LibreLink",
                device_id="1D48A10E-DDFB-4888-8158-026F08814832",
                record_type="0",
                notes=None
            )
        ]
        
        # Configure mock
        mock_repository.get_by_user_id.return_value = (glucose_levels, len(glucose_levels))
        
        # Execute
        result = await service.export_to_json(user_id)
        
        # Assert
        assert len(result) == 1
        assert result[0]["id"] == glucose_id
        assert result[0]["glucose_value"] == 77