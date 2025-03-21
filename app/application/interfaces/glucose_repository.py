"""Repository interface for glucose levels."""
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import UUID

from app.domain.models.glucose_level import GlucoseLevel


class IGlucoseRepository:
    """Interface for glucose repository operations."""
    
    async def get_by_id(self, glucose_id: UUID) -> Optional[GlucoseLevel]:
        """
        Get a glucose level by ID.
        
        Args:
            glucose_id: The ID of the glucose level
            
        Returns:
            The glucose level if found, None otherwise
        """
        raise NotImplementedError
    
    async def get_by_user_id(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ) -> Tuple[List[GlucoseLevel], int]:
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
        raise NotImplementedError
    
    async def create(self, glucose_level: GlucoseLevel) -> GlucoseLevel:
        """
        Create a new glucose level.
        
        Args:
            glucose_level: The glucose level to create
            
        Returns:
            The created glucose level
        """
        raise NotImplementedError
    
    async def create_many(self, glucose_levels: List[GlucoseLevel]) -> List[GlucoseLevel]:
        """
        Create multiple glucose levels at once.
        
        Args:
            glucose_levels: List of glucose levels to create
            
        Returns:
            List of created glucose levels
        """
        raise NotImplementedError
    
    async def update(self, glucose_level: GlucoseLevel) -> Optional[GlucoseLevel]:
        """
        Update a glucose level.
        
        Args:
            glucose_level: The glucose level to update
            
        Returns:
            The updated glucose level if found, None otherwise
        """
        raise NotImplementedError
    
    async def delete(self, glucose_id: UUID) -> bool:
        """
        Delete a glucose level.
        
        Args:
            glucose_id: The ID of the glucose level to delete
            
        Returns:
            True if deleted, False if not found
        """
        raise NotImplementedError