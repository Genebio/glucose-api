# Glucose Levels API

An API service for storing and retrieving glucose level measurements.

## Architecture

This project follows Onion Architecture principles:

- **Domain Layer**: Core business models and logic
- **Application Layer**: Application services and interfaces
- **Infrastructure Layer**: Data persistence and external services
- **Interface Layer**: API endpoints and controllers

## Features

- Store glucose level measurements
- Retrieve glucose levels with filtering, pagination, and sorting
- Import glucose levels from CSV files
- Export glucose levels to CSV, JSON, and Excel formats
- Documented API with OpenAPI/Swagger UI

## Technologies

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- Pandas
- SQLite
- Docker
- Kubernetes

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Kubernetes (for remote deployment)

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/Genebio/glucose-api.git
cd glucose-api
```

2. Install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the application locally:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

### Using Docker Compose (Local)

For local development and testing with Docker:

```bash
docker-compose up -d
```

To import sample data:

```bash
docker exec glucose-api python scripts/import_data.py
```

### Remote Deployment

This application is deployed on Render.com. You can access the demo at:
- API Documentation: https://glucose-api.onrender.com/docs
- Health Check: https://glucose-api.onrender.com/health

To deploy your own instance:

1. Push your code to GitHub

2. Connect your repository to Render:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" and select "Blueprint" 
   - Connect your GitHub repository
   - Render will detect the configuration automatically

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

- `GET /api/v1/levels/`: Get a list of glucose levels for a user
  - Query parameters:
    - `user_id`: UUID (required)
    - `start`: ISO datetime (optional)
    - `stop`: ISO datetime (optional)
    - `page`: int (default: 1)
    - `page_size`: int (default: 100, max: 1000)
    - `sort_by`: string (default: "timestamp")
    - `sort_order`: string (default: "desc")

- `GET /api/v1/levels/{glucose_id}/`: Get a specific glucose level by ID

- `POST /api/v1/levels/`: Create a new glucose level

- `POST /api/v1/levels/import`: Import glucose levels from a CSV file
  - Form data:
    - `user_id`: UUID (required)
    - `file`: CSV file (required)

- `GET /api/v1/levels/export/csv`: Export glucose levels to CSV
- `GET /api/v1/levels/export/json`: Export glucose levels to JSON
- `GET /api/v1/levels/export/excel`: Export glucose levels to Excel

## Data Import

The application comes with a script to import data from CSV files:

```bash
python scripts/import_data.py --data-dir ./data
```

Or import a specific file:

```bash
python scripts/import_data.py --file ./data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv
```

## Running Tests

```bash
pytest
```

## Deployment Architecture

The application is designed for both local and cloud-based deployment:

### Local Deployment
- Uses Docker Compose for local containerization
- Persistent volume for SQLite database

### Cloud Deployment
- Kubernetes-based deployment with 2 replicas for high availability
- Persistent volume claim for shared database storage
- Service with LoadBalancer for external access
- Health probes for reliable container management

## Production Considerations

For a production environment:

1. Replace SQLite with a more robust database like PostgreSQL
2. Add authentication and authorization
3. Implement API rate limiting
4. Set up monitoring and logging
5. Configure TLS for secure communication
6. Implement CI/CD pipelines for automated testing and deployment