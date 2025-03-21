"""SQLAlchemy repository implementation for glucose levels."""
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.application.interfaces.glucose_repository import IGlucoseRepository
from app.domain.models.glucose_level import GlucoseLevel as GlucoseLevelDomain
from app.infrastructure.database.models import GlucoseLevel as GlucoseLevelDB


class SQLAlchemyGlucoseRepository(IGlucoseRepository):
    """SQLAlchemy implementation of the glucose repository interface."""
    
    def __init__(self, db: Session):
        """
        Initialize the repository.
        
        Args:
            db: The database session
        """
        self.db = db
    
    async def get_by_id(self, glucose_id: UUID) -> Optional[GlucoseLevelDomain]:
        """
        Get a glucose level by ID.
        
        Args:
            glucose_id: The ID of the glucose level
            
        Returns:
            The glucose level if found, None otherwise
        """
        result = self.db.query(GlucoseLevelDB).filter(GlucoseLevelDB.id == str(glucose_id)).first()
        if not result:
            return None
        return GlucoseLevelDomain.model_validate(result)
    
    async def get_by_user_id(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ) -> Tuple[List[GlucoseLevelDomain], int]:
        """
        Get glucose levels for a user with pagination and filtering.
        
        Args:
            user_id: The ID of the user
            start_time: Optional start time filter
            end_time: Optional end time filter
            page: Page number (1-based)
            page_size: Number of items per page
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')
            
        Returns:
            Tuple containing list of glucose levels and total count
        """
        query = self.db.query(GlucoseLevelDB).filter(GlucoseLevelDB.user_id == str(user_id))
        
        # Apply time filters if provided
        if start_time:
            query = query.filter(GlucoseLevelDB.timestamp >= start_time)
        if end_time:
            query = query.filter(GlucoseLevelDB.timestamp <= end_time)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if hasattr(GlucoseLevelDB, sort_by):
            sort_column = getattr(GlucoseLevelDB, sort_by)
            if sort_order.lower() == "asc":
                query = query.order_by(asc(sort_column))
            else:
                query = query.order_by(desc(sort_column))
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Execute query and convert to domain model
        results = query.all()
        domain_results = [GlucoseLevelDomain.model_validate(result) for result in results]
        
        return domain_results, total
    
    async def create(self, glucose_level: GlucoseLevelDomain) -> GlucoseLevelDomain:
        """
        Create a new glucose level.
        
        Args:
            glucose_level: The glucose level to create
            
        Returns:
            The created glucose level
        """
        db_glucose = GlucoseLevelDB(
            id=str(glucose_level.id),
            user_id=str(glucose_level.user_id),
            timestamp=glucose_level.timestamp,
            glucose_value=glucose_level.glucose_value,
            device_type=glucose_level.device_type,
            device_id=glucose_level.device_id,
            record_type=glucose_level.record_type,
            notes=glucose_level.notes,
            created_at=glucose_level.created_at,
            updated_at=glucose_level.updated_at
        )
        
        self.db.add(db_glucose)
        self.db.commit()
        self.db.refresh(db_glucose)
        
        return GlucoseLevelDomain.model_validate(db_glucose)
    
    async def create_many(self, glucose_levels: List[GlucoseLevelDomain]) -> List[GlucoseLevelDomain]:
        """
        Create multiple glucose levels at once.
        
        Args:
            glucose_levels: List of glucose levels to create
            
        Returns:
            List of created glucose levels
        """
        db_glucose_levels = [
            GlucoseLevelDB(
                id=str(gl.id),
                user_id=str(gl.user_id),
                timestamp=gl.timestamp,
                glucose_value=gl.glucose_value,
                device_type=gl.device_type,
                device_id=gl.device_id,
                record_type=gl.record_type,
                notes=gl.notes,
                created_at=gl.created_at,
                updated_at=gl.updated_at
            )
            for gl in glucose_levels
        ]
        
        self.db.add_all(db_glucose_levels)
        self.db.commit()
        
        # Return the domain models
        return glucose_levels
    
    async def update(self, glucose_level: GlucoseLevelDomain) -> Optional[GlucoseLevelDomain]:
        """
        Update a glucose level.
        
        Args:
            glucose_level: The glucose level to update
            
        Returns:
            The updated glucose level if found, None otherwise
        """
        db_glucose = self.db.query(GlucoseLevelDB).filter(GlucoseLevelDB.id == str(glucose_level.id)).first()
        if not db_glucose:
            return None
        
        # Update fields
        db_glucose.user_id = str(glucose_level.user_id)
        db_glucose.timestamp = glucose_level.timestamp
        db_glucose.glucose_value = glucose_level.glucose_value
        db_glucose.device_type = glucose_level.device_type
        db_glucose.device_id = glucose_level.device_id
        db_glucose.record_type = glucose_level.record_type
        db_glucose.notes = glucose_level.notes
        db_glucose.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_glucose)
        
        return GlucoseLevelDomain.model_validate(db_glucose)
    
    async def delete(self, glucose_id: UUID) -> bool:
        """
        Delete a glucose level.
        
        Args:
            glucose_id: The ID of the glucose level to delete
            
        Returns:
            True if deleted, False if not found
        """
        db_glucose = self.db.query(GlucoseLevelDB).filter(GlucoseLevelDB.id == str(glucose_id)).first()
        if not db_glucose:
            return False
        
        self.db.delete(db_glucose)
        self.db.commit()
        
        return True