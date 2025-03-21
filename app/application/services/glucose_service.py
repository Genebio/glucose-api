"""Service layer for glucose level operations."""
import csv
import uuid
from datetime import datetime
from io import StringIO
from typing import List, Optional
from uuid import UUID

import pandas as pd

from app.application.interfaces.glucose_repository import IGlucoseRepository
from app.domain.models.glucose_level import GlucoseLevel
from app.domain.schemas.glucose_level import (
    GlucoseLevelCreate,
    GlucoseLevelList,
    GlucoseLevelCSVRow,
)


class GlucoseService:
    """Service for handling glucose level operations."""
    
    def __init__(self, repository: IGlucoseRepository):
        """
        Initialize the service.
        
        Args:
            repository: The glucose repository
        """
        self.repository = repository
    
    async def get_glucose_level(self, glucose_id: UUID) -> Optional[GlucoseLevel]:
        """
        Get a glucose level by ID.
        
        Args:
            glucose_id: The ID of the glucose level
            
        Returns:
            The glucose level if found, None otherwise
        """
        return await self.repository.get_by_id(glucose_id)
    
    async def get_glucose_levels(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
        sort_by: str = "timestamp",
        sort_order: str = "desc"
    ) -> GlucoseLevelList:
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
            Paginated list of glucose levels
        """
        items, total = await self.repository.get_by_user_id(
            user_id, start_time, end_time, page, page_size, sort_by, sort_order
        )
        
        total_pages = (total + page_size - 1) // page_size
        
        return GlucoseLevelList(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    
    async def create_glucose_level(self, glucose_data: GlucoseLevelCreate) -> GlucoseLevel:
        """
        Create a new glucose level.
        
        Args:
            glucose_data: Data for the new glucose level
            
        Returns:
            The created glucose level
        """
        glucose_level = GlucoseLevel(
            id=uuid.uuid4(),
            user_id=glucose_data.user_id,
            timestamp=glucose_data.timestamp,
            glucose_value=glucose_data.glucose_value,
            device_type=glucose_data.device_type,
            device_id=glucose_data.device_id,
            record_type=glucose_data.record_type,
            notes=glucose_data.notes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        return await self.repository.create(glucose_level)
    
    async def import_from_csv(self, file_path: str, user_id: UUID) -> int:
        """
        Import glucose levels from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            user_id: User ID to associate with imported data
            
        Returns:
            Number of imported records
        """
        try:
            print(f"Importing data from {file_path} for user {user_id}")
            
            # Read CSV file - handle different formats based on filenames
            try:
                # First try with standard format (2 header rows)
                df = pd.read_csv(file_path, encoding='utf-8', skiprows=2)
            except Exception as e:
                try:
                    # Try without skipping rows
                    df = pd.read_csv(file_path, encoding='utf-8')
                except Exception as e2:
                    print(f"Error reading CSV file: {e2}")
                    return 0
            
            # Pre-process the dataframe
            if 'Glukosewert-Verlauf mg/dL' not in df.columns:
                print(f"Missing required column 'Glukosewert-Verlauf mg/dL' in {file_path}")
                return 0
                
            # Convert required fields and handle NaN values
            # Convert record type to string
            if 'Aufzeichnungstyp' in df.columns:
                df['Aufzeichnungstyp'] = df['Aufzeichnungstyp'].astype(str)
                
            # Handle NaN values
            for col in df.columns:
                if col != 'Glukosewert-Verlauf mg/dL':  # Don't fill glucose values
                    if df[col].dtype == 'object' or df[col].dtype == 'float64':
                        df[col] = df[col].fillna("")
            
            # Process data
            glucose_levels = []
            for idx, row in df.iterrows():
                # Skip rows with empty glucose values
                if pd.isna(row.get('Glukosewert-Verlauf mg/dL')):
                    continue
                
                try:
                    # Clean row data
                    row_dict = {}
                    for col in row.index:
                        # Handle NaN/None values
                        if pd.isna(row[col]) or row[col] is None:
                            if col == 'Notizen':  # For optional string fields
                                row_dict[col] = ""
                            elif col == 'Aufzeichnungstyp':  # For record type
                                row_dict[col] = "0"
                            else:
                                row_dict[col] = ""
                        else:
                            row_dict[col] = row[col]
                    
                    # Create simplified dictionary with just what we need
                    simple_row = {
                        "Gerät": str(row_dict.get('Gerät', "")),
                        "Seriennummer": str(row_dict.get('Seriennummer', "")),
                        "Gerätezeitstempel": str(row_dict.get('Gerätezeitstempel', "")),
                        "Aufzeichnungstyp": str(row_dict.get('Aufzeichnungstyp', "0")),
                        "Glukosewert-Verlauf mg/dL": float(row_dict.get('Glukosewert-Verlauf mg/dL', 0)),
                        "Notizen": str(row_dict.get('Notizen', ""))
                    }
                    
                    # Parse the timestamp
                    timestamp_str = simple_row["Gerätezeitstempel"]
                    timestamp = None
                    
                    # Try different date formats
                    date_formats = [
                        "%d-%m-%Y %H:%M",  # 18-02-2021 10:57
                        "%Y-%m-%d %H:%M:%S",  # 2021-02-18 10:57:00
                        "%Y-%m-%d %H:%M"  # 2021-02-18 10:57
                    ]
                    
                    for format in date_formats:
                        try:
                            timestamp = datetime.strptime(timestamp_str, format)
                            break
                        except (ValueError, TypeError):
                            continue
                    
                    if timestamp is None:
                        print(f"Unable to parse timestamp: {timestamp_str}, skipping row {idx}")
                        continue
                    
                    # Create glucose level directly
                    glucose_level = GlucoseLevel(
                        id=uuid.uuid4(),
                        user_id=user_id,
                        timestamp=timestamp,
                        glucose_value=float(simple_row["Glukosewert-Verlauf mg/dL"]),
                        device_type=simple_row["Gerät"],
                        device_id=simple_row["Seriennummer"],
                        record_type=simple_row["Aufzeichnungstyp"],
                        notes=simple_row["Notizen"] if simple_row["Notizen"] else None,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    glucose_levels.append(glucose_level)
                except Exception as e:
                    # Log error but continue processing
                    print(f"Error processing row {idx}: {e}")
            
            print(f"Processed {len(glucose_levels)} valid records from {file_path}")
            
            # Save to database
            if glucose_levels:
                print(f"Saving {len(glucose_levels)} records to database")
                await self.repository.create_many(glucose_levels)
                print(f"Successfully saved {len(glucose_levels)} records")
            else:
                print(f"No valid records found in {file_path}")
            
            return len(glucose_levels)
        except Exception as e:
            print(f"Error importing {file_path}: {str(e)}")
            return 0
    
    async def export_to_csv(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> str:
        """
        Export glucose levels to CSV.
        
        Args:
            user_id: The ID of the user
            start_time: Optional start time filter
            end_time: Optional end time filter
            
        Returns:
            CSV string
        """
        # Get all data for the user without pagination
        items, _ = await self.repository.get_by_user_id(
            user_id, start_time, end_time, page=1, page_size=1000000, sort_by="timestamp", sort_order="asc"
        )
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "ID", "User ID", "Timestamp", "Glucose Value (mg/dL)",
            "Device Type", "Device ID", "Record Type", "Notes"
        ])
        
        # Write data
        for item in items:
            writer.writerow([
                item.id, item.user_id, item.timestamp, item.glucose_value,
                item.device_type, item.device_id, item.record_type, item.notes
            ])
        
        return output.getvalue()
    
    async def export_to_json(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[dict]:
        """
        Export glucose levels to JSON.
        
        Args:
            user_id: The ID of the user
            start_time: Optional start time filter
            end_time: Optional end time filter
            
        Returns:
            List of glucose level dictionaries
        """
        # Get all data for the user without pagination
        items, _ = await self.repository.get_by_user_id(
            user_id, start_time, end_time, page=1, page_size=1000000, sort_by="timestamp", sort_order="asc"
        )
        
        # Convert to JSON
        return [item.model_dump() for item in items]
    
    async def export_to_excel(
        self,
        user_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> bytes:
        """
        Export glucose levels to Excel.
        
        Args:
            user_id: The ID of the user
            start_time: Optional start time filter
            end_time: Optional end time filter
            
        Returns:
            Excel file as bytes
        """
        # Get all data for the user without pagination
        items, _ = await self.repository.get_by_user_id(
            user_id, start_time, end_time, page=1, page_size=1000000, sort_by="timestamp", sort_order="asc"
        )
        
        # Convert to pandas DataFrame
        data = [
            {
                "ID": str(item.id),
                "User ID": str(item.user_id),
                "Timestamp": item.timestamp,
                "Glucose Value (mg/dL)": item.glucose_value,
                "Device Type": item.device_type,
                "Device ID": item.device_id,
                "Record Type": item.record_type,
                "Notes": item.notes
            }
            for item in items
        ]
        df = pd.DataFrame(data)
        
        # Export to Excel
        output = StringIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Glucose Levels")
        
        return output.getvalue().encode("utf-8")