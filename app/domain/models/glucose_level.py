"""Domain model for glucose levels."""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class GlucoseLevel(BaseModel):
    """Domain model representing a glucose level measurement."""
    
    id: UUID
    user_id: UUID
    timestamp: datetime
    glucose_value: float = Field(gt=0)
    device_type: str
    device_id: str
    record_type: str | None = None
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic model configuration."""
        from_attributes = True