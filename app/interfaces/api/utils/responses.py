"""API response utilities."""
from typing import Any, Dict, Generic, Optional, TypeVar
from fastapi import HTTPException, status
from pydantic import BaseModel


T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Standard API response format."""
    
    success: bool
    message: str
    data: Optional[T] = None


def success_response(message: str, data: Any = None) -> Dict:
    """
    Create a success response.
    
    Args:
        message: Success message
        data: Response data
        
    Returns:
        Response dictionary
    """
    return APIResponse(success=True, message=message, data=data).model_dump()


def error_response(message: str) -> Dict:
    """
    Create an error response.
    
    Args:
        message: Error message
        
    Returns:
        Response dictionary
    """
    return APIResponse(success=False, message=message).model_dump()


def not_found_exception(detail: str = "Resource not found") -> HTTPException:
    """
    Create a 404 Not Found exception.
    
    Args:
        detail: Error detail
        
    Returns:
        HTTP exception
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


def bad_request_exception(detail: str = "Bad request") -> HTTPException:
    """
    Create a 400 Bad Request exception.
    
    Args:
        detail: Error detail
        
    Returns:
        HTTP exception
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )