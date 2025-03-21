"""API v1 routes module."""
from fastapi import APIRouter

from app.interfaces.api.v1.glucose_levels import router as glucose_router

router = APIRouter(prefix="/api/v1")
router.include_router(glucose_router)

__all__ = ["router"]