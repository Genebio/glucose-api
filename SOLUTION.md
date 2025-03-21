# Una Health Backend Challenge Solution

## Deployed Demo

A live demo of this application is available at:
- API Documentation: https://glucose-api.onrender.com/docs
- Health Check: https://glucose-api.onrender.com/health
- Example Endpoint: https://glucose-api.onrender.com/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc

## Project Structure and Architecture

This solution implements a glucose levels API using FastAPI, SQLAlchemy, and SQLite. The project follows Onion Architecture principles:

1. **Domain Layer**
   - Contains core business models and schemas
   - Defines the GlucoseLevel entity and validation rules

2. **Application Layer**
   - Defines interfaces (repository interfaces)
   - Implements service layer with business logic
   - Handles use cases like importing/exporting data

3. **Infrastructure Layer**
   - Implements repositories using SQLAlchemy
   - Manages database connections and models
   - Provides persistence mechanisms

4. **Interface Layer**
   - Implements API endpoints with FastAPI
   - Handles HTTP requests/responses
   - Provides utility functions for pagination, error handling, etc.

## Key Features Implemented

1. **API Endpoints**
   - `GET /api/v1/levels/` - List glucose levels with filtering, pagination, and sorting
   - `GET /api/v1/levels/{id}/` - Get a specific glucose level by ID
   - `POST /api/v1/levels/` - Create a new glucose level
   - `POST /api/v1/levels/import` - Import glucose levels from CSV files
   - Export endpoints for CSV, JSON, and Excel formats

2. **Data Management**
   - SQLite database with SQLAlchemy ORM
   - CSV data import/parsing with Pandas
   - Data validation with Pydantic models

3. **Error Handling**
   - Comprehensive error handling throughout the application
   - Consistent API response format
   - Validation of query parameters

4. **Testing**
   - Unit tests for service layer
   - Unit tests for API endpoints
   - Fixtures for database testing

5. **Deployment Options**
   - Docker containerization for local development
   - Cloud deployment via Render.com (currently live)

## Technical Decisions

1. **SQLite**: Used for simplicity and easy portability
2. **FastAPI**: Modern, high-performance web framework with auto-generated docs
3. **Pydantic**: For data validation and serialization/deserialization
4. **Pandas**: For efficient CSV processing and Excel export
5. **Onion Architecture**: For maintainable, testable, and loosely coupled code

## Running the Application

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python run.py
   ```
   
3. Import sample data:
   ```
   python scripts/import_data.py --data-dir ./data
   ```

4. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Future Improvements

1. Add authentication and authorization
2. Implement additional data validation and error handling
3. Add caching for frequently accessed data
4. Implement more comprehensive logging
5. Add database migrations for schema changes
6. Implement real-time data streaming