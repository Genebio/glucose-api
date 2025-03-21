"""SQLAlchemy database models."""
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.sqlite import BLOB

from app.infrastructure.database.connection import Base


class GlucoseLevel(Base):
    """SQLAlchemy model for glucose levels."""
    
    __tablename__ = "glucose_levels"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    glucose_value = Column(Float, nullable=False)
    device_type = Column(String(255), nullable=False)
    device_id = Column(String(255), nullable=False)
    record_type = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """Return string representation of the glucose level."""
        return (
            f"GlucoseLevel(id={self.id}, user_id={self.user_id}, "
            f"timestamp={self.timestamp}, glucose_value={self.glucose_value})"
        )