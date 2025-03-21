#!/usr/bin/env python
"""Script to import glucose data from CSV files."""
import argparse
import asyncio
import os
import sys
import uuid
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session

from app.application.services import GlucoseService
from app.infrastructure.database import SessionLocal, Base, engine
from app.infrastructure.repositories import SQLAlchemyGlucoseRepository

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)


async def import_file(file_path: str, user_id: str, db: Session):
    """
    Import glucose levels from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        user_id: User ID to associate with data
        db: Database session
    
    Returns:
        Number of imported records
    """
    repository = SQLAlchemyGlucoseRepository(db)
    service = GlucoseService(repository)
    
    try:
        user_uuid = uuid.UUID(user_id)
        count = await service.import_from_csv(file_path, user_uuid)
        print(f"Imported {count} records from {file_path}")
        return count
    except Exception as e:
        print(f"Error importing {file_path}: {str(e)}")
        return 0


async def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Import glucose data from CSV files")
    parser.add_argument("--data-dir", required=False, default="./data", help="Directory with CSV files")
    parser.add_argument("--file", required=False, help="Specific CSV file to import")
    
    args = parser.parse_args()
    
    # Get database session
    db = SessionLocal()
    
    try:
        total_imported = 0
        
        if args.file:
            # Import specific file
            if not os.path.exists(args.file):
                print(f"File not found: {args.file}")
                return
            
            # Use filename as user ID
            file_name = os.path.basename(args.file)
            user_id = os.path.splitext(file_name)[0]
            
            count = await import_file(args.file, user_id, db)
            total_imported += count
        else:
            # Import all files in directory
            data_dir = args.data_dir
            if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
                print(f"Data directory not found: {data_dir}")
                return
            
            for file_name in os.listdir(data_dir):
                if file_name.endswith(".csv"):
                    file_path = os.path.join(data_dir, file_name)
                    
                    # Use filename as user ID
                    user_id = os.path.splitext(file_name)[0]
                    
                    count = await import_file(file_path, user_id, db)
                    total_imported += count
        
        print(f"Total records imported: {total_imported}")
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())