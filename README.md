# SDA Backend API

FastAPI backend application with SQLAlchemy 2.0, Pydantic v2, and PostgreSQL.

## Requirements

- Python 3.11+
- PostgreSQL
- Poetry (recommended) or pip

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with:
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sda_db
```

5. Initialize the database:
```bash
alembic upgrade head
```

6. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── core/           # Core configuration
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
├── crud/          # Database operations
├── routers/       # API endpoints
└── main.py        # FastAPI application
```

## Features

- FastAPI CRUD operations
- SQLAlchemy 2.0 ORM
- Pydantic v2 validation
- PostgreSQL database
- Alembic migrations
- CORS middleware
- OpenAPI documentation
