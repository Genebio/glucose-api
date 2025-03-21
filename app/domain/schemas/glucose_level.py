"""Schemas for glucose level data."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class GlucoseLevelBase(BaseModel):
    """Base schema for glucose level data."""
    
    timestamp: datetime
    glucose_value: float = Field(gt=0, description="Glucose value in mg/dL")
    device_type: str
    device_id: str
    record_type: Optional[str] = None
    notes: Optional[str] = None


class GlucoseLevelCreate(GlucoseLevelBase):
    """Schema for creating a new glucose level."""
    
    user_id: UUID


class GlucoseLevel(GlucoseLevelBase):
    """Schema for retrieving a glucose level."""
    
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class GlucoseLevelList(BaseModel):
    """Schema for a paginated list of glucose levels."""
    
    items: List[GlucoseLevel]
    total: int
    page: int
    page_size: int
    total_pages: int


class GlucoseLevelImport(BaseModel):
    """Schema for importing glucose levels from CSV files."""
    
    file_path: str
    user_id: UUID


# Class for direct modeling of CSV data
class GlucoseLevelCSVRow(BaseModel):
    """Schema for a row in a glucose level CSV file."""
    
    device_type: str = Field(alias="Gerät")
    device_id: str = Field(alias="Seriennummer")
    timestamp: str = Field(alias="Gerätezeitstempel")  # Keep as string, will convert manually
    record_type: str = Field(alias="Aufzeichnungstyp")
    glucose_value: float = Field(alias="Glukosewert-Verlauf mg/dL")
    notes: Optional[str] = Field(default="", alias="Notizen")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="ignore",  # Ignore extra fields
    )