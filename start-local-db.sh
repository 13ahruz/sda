#!/bin/bash

echo "🚀 Starting SDA Backend Local Development Environment"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "📦 Starting PostgreSQL and Redis containers..."
docker-compose -f docker-compose.local.yml up -d

echo "⏳ Waiting for database to be ready..."
sleep 10

# Check if database is ready
while ! docker exec sda_postgres_local pg_isready -U postgres > /dev/null 2>&1; do
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 2
done

echo "✅ Database is ready!"

echo "📋 Container Status:"
docker-compose -f docker-compose.local.yml ps

echo ""
echo "🔗 Connection Information:"
echo "PostgreSQL: localhost:5432"
echo "  - Database: sda_local_db"
echo "  - Username: postgres"
echo "  - Password: postgres123"
echo ""
echo "Redis: localhost:6379"
echo "  - Password: redis123"
echo ""
echo "🏃‍♂️ To run the FastAPI server locally:"
echo "1. Install Python dependencies: pip install -r requirements.txt"
echo "2. Run migrations: alembic upgrade head"
echo "3. Start server: uvicorn app.main:app --reload --port 8000"
echo ""
echo "🛑 To stop containers: docker-compose -f docker-compose.local.yml down"