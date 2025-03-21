"""API routes for glucose levels."""
import os
from datetime import datetime
from io import BytesIO
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.application.services import GlucoseService
from app.domain.schemas import GlucoseLevelCreate, GlucoseLevel, GlucoseLevelList
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SQLAlchemyGlucoseRepository
from app.interfaces.api.utils import (
    success_response,
    error_response,
    not_found_exception,
    bad_request_exception,
    validate_pagination,
    parse_date_param
)


router = APIRouter(prefix="/levels", tags=["glucose_levels"])


@router.get("/", response_model=GlucoseLevelList)
async def get_glucose_levels(
    user_id: UUID = Query(..., description="ID of the user"),
    start: Optional[str] = Query(None, description="Start timestamp (ISO format)"),
    stop: Optional[str] = Query(None, description="End timestamp (ISO format)"),
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    page_size: Optional[int] = Query(100, ge=1, le=1000, description="Page size"),
    sort_by: Optional[str] = Query("timestamp", description="Field to sort by"),
    sort_order: Optional[str] = Query("desc", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of glucose levels for a user.
    
    Args:
        user_id: ID of the user
        start: Optional start timestamp (ISO format)
        stop: Optional end timestamp (ISO format)
        page: Page number (1-based)
        page_size: Number of items per page
        sort_by: Field to sort by
        sort_order: Sort order ('asc' or 'desc')
        db: Database session
        
    Returns:
        Paginated list of glucose levels
    """
    # Validate parameters
    page, page_size = validate_pagination(page, page_size)
    
    if sort_by not in ["id", "timestamp", "glucose_value", "created_at", "updated_at"]:
        sort_by = "timestamp"
    
    if sort_order not in ["asc", "desc"]:
        sort_order = "desc"
    
    # Parse date parameters
    try:
        start_time = parse_date_param(start)
        end_time = parse_date_param(stop)
    except ValueError as e:
        raise bad_request_exception(str(e))
    
    # Create service
    repository = SQLAlchemyGlucoseRepository(db)
    service = GlucoseService(repository)
    
    # Get glucose levels
    return await service.get_glucose_levels(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/{glucose_id}", response_model=GlucoseLevel)
async def get_glucose_level(
    glucose_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a glucose level by ID.
    
    Args:
        glucose_id: ID of the glucose level
        db: Database session
        
    Returns:
        Glucose level data
        
    Raises:
        HTTPException: If glucose level not found
    """
    # Create service
    repository = SQLAlchemyGlucoseRepository(db)
    service = GlucoseService(repository)
    
    # Get glucose level
    glucose_level = await service.get_glucose_level(glucose_id)
    if not glucose_level:
        raise not_found_exception(f"Glucose level with ID {glucose_id} not found")
    
    return glucose_level


@router.post("/", response_model=GlucoseLevel, status_code=status.HTTP_201_CREATED)
async def create_glucose_level(
    glucose_data: GlucoseLevelCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new glucose level.
    
    Args:
        glucose_data: Glucose level data
        db: Database session
        
    Returns:
        Created glucose level
    """
    # Create service
    repository = SQLAlchemyGlucoseRepository(db)
    service = GlucoseService(repository)
    
    # Create glucose level
    return await service.create_glucose_level(glucose_data)


@router.post("/import", response_model=dict)
async def import_glucose_levels(
    user_id: UUID = Form(..., description="ID of the user"),
    file: UploadFile = File(..., description="CSV file with glucose levels"),
    db: Session = Depends(get_db)
):
    """
    Import glucose levels from a CSV file.
    
    Args:
        user_id: ID of the user
        file: CSV file with glucose levels
        db: Database session
        
    Returns:
        Import result
    """
    # Save uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    try:
        # Save file
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Create service
        repository = SQLAlchemyGlucoseRepository(db)
        service = GlucoseService(repository)
        
        # Import data
        imported_count = await service.import_from_csv(temp_file_path, user_id)
        
        return success_response(
            message=f"Successfully imported {imported_count} glucose level records",
            data={"imported_count": imported_count}
        )
    except Exception as e:
        raise bad_request_exception(f"Error importing data: {str(e)}")
    finally:
        # Clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@router.get("/export/csv")
async def export_glucose_levels_csv(
    user_id: UUID = Query(..., description="ID of the user"),
    start: Optional[str] = Query(None, description="Start timestamp (ISO format)"),
    stop: Optional[str] = Query(None, description="End timestamp (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Export glucose levels to CSV for a user.
    
    Args:
        user_id: ID of the user
        start: Optional start timestamp (ISO format)
        stop: Optional end timestamp (ISO format)
        db: Database session
        
    Returns:
        CSV file
    """
    # Parse date parameters
    try:
        start_time = parse_date_param(start)
        end_time = parse_date_param(stop)
    except ValueError as e:
        raise bad_request_exception(str(e))
    
    # Create service
    repository = SQLAlchemyGlucoseRepository(db)
    service = GlucoseService(repository)
    
    # Export data
    csv_data = await service.export_to_csv(user_id, start_time, end_time)
    
    # Return as downloadable file
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=glucose_levels_{user_id}.csv"}
    )


@router.get("/export/json")
async def export_glucose_levels_json(
    user_id: UUID = Query(..., description="ID of the user"),
    start: Optional[str] = Query(None, description="Start timestamp (ISO format)"),
    stop: Optional[str] = Query(None, description="End timestamp (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Export glucose levels to JSON for a user.
    
    Args:
        user_id: ID of the user
        start: Optional start timestamp (ISO format)
        stop: Optional end timestamp (ISO format)
        db: Database session
        
    Returns:
        JSON data
    """
    # Parse date parameters
    try:
        start_time = parse_date_param(start)
        end_time = parse_date_param(stop)
    except ValueError as e:
        raise bad_request_exception(str(e))
    
    # Create service
    repository = SQLAlchemyGlucoseRepository(db)
    service = GlucoseService(repository)
    
    # Export data
    return await service.export_to_json(user_id, start_time, end_time)


@router.get("/export/excel")
async def export_glucose_levels_excel(
    user_id: UUID = Query(..., description="ID of the user"),
    start: Optional[str] = Query(None, description="Start timestamp (ISO format)"),
    stop: Optional[str] = Query(None, description="End timestamp (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Export glucose levels to Excel for a user.
    
    Args:
        user_id: ID of the user
        start: Optional start timestamp (ISO format)
        stop: Optional end timestamp (ISO format)
        db: Database session
        
    Returns:
        Excel file
    """
    # Parse date parameters
    try:
        start_time = parse_date_param(start)
        end_time = parse_date_param(stop)
    except ValueError as e:
        raise bad_request_exception(str(e))
    
    # Create service
    repository = SQLAlchemyGlucoseRepository(db)
    service = GlucoseService(repository)
    
    # Export data
    excel_data = await service.export_to_excel(user_id, start_time, end_time)
    
    # Return as downloadable file
    return StreamingResponse(
        BytesIO(excel_data),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=glucose_levels_{user_id}.xlsx"}
    )