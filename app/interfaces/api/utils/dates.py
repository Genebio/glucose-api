"""API date utilities."""
from datetime import datetime
from typing import Optional


def parse_date_param(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parse date string parameter.
    
    Args:
        date_str: Date string in ISO format (e.g., '2021-02-18T10:57:00')
        
    Returns:
        Parsed datetime or None if input is None
    """
    if not date_str:
        return None
    
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        # Try with different format
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Expected ISO format (e.g., '2021-02-18T10:57:00').")