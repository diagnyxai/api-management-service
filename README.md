# API Management Service

API management service for the Diagnyx platform, providing API registration, documentation, and analytics integration.

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: PostgreSQL
- **Port**: 8086 (HTTP)

## Features

- API registration and configuration
- API documentation management
- API versioning
- API analytics integration

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/apis` | GET | List all registered APIs |
| `/api/v1/apis` | POST | Register a new API |
| `/api/v1/apis/{api_id}` | GET | Get API details by ID |
| `/health` | GET | Service health check |
| `/service-status` | GET | Service and database status |

## Running Locally

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8086
```

## Database Configuration

The service is configured to use PostgreSQL:

```python
DATABASE_URL = "postgresql://dev:dev@localhost:5432/dgx-dev"
```

## API Documentation

When running, API documentation is available at:
- Swagger UI: http://localhost:8086/docs
- ReDoc: http://localhost:8086/redoc 