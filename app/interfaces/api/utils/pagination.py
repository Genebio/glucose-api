"""API pagination utilities."""
from typing import Optional

from app.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


def validate_pagination(
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> tuple[int, int]:
    """
    Validate pagination parameters.
    
    Args:
        page: Page number
        page_size: Page size
        
    Returns:
        Tuple of (page, page_size)
    """
    # Default values
    if page is None:
        page = 1
    if page_size is None:
        page_size = DEFAULT_PAGE_SIZE
    
    # Validation
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = DEFAULT_PAGE_SIZE
    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE
    
    return page, page_size