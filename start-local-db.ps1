# PowerShell script for starting local development environment
Write-Host "🚀 Starting SDA Backend Local Development Environment" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Starting PostgreSQL and Redis containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.local.yml up -d

Write-Host "⏳ Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if database is ready
$maxAttempts = 30
$attempt = 0
do {
    $attempt++
    try {
        $result = docker exec sda_postgres_local pg_isready -U postgres 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Database is ready!" -ForegroundColor Green
            break
        }
    } catch {
        # Continue waiting
    }
    
    if ($attempt -ge $maxAttempts) {
        Write-Host "❌ Database failed to start after $maxAttempts attempts" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "⏳ Waiting for PostgreSQL to be ready... (attempt $attempt/$maxAttempts)" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
} while ($true)

Write-Host "📋 Container Status:" -ForegroundColor Cyan
docker-compose -f docker-compose.local.yml ps

Write-Host ""
Write-Host "🔗 Connection Information:" -ForegroundColor Cyan
Write-Host "PostgreSQL: localhost:5432" -ForegroundColor White
Write-Host "  - Database: sda_local_db" -ForegroundColor Gray
Write-Host "  - Username: postgres" -ForegroundColor Gray
Write-Host "  - Password: postgres123" -ForegroundColor Gray
Write-Host ""
Write-Host "Redis: localhost:6379" -ForegroundColor White
Write-Host "  - Password: redis123" -ForegroundColor Gray
Write-Host ""
Write-Host "🏃‍♂️ To run the FastAPI server locally:" -ForegroundColor Cyan
Write-Host "1. Install Python dependencies: pip install -r requirements.txt" -ForegroundColor White
Write-Host "2. Copy environment: copy .env.local .env" -ForegroundColor White
Write-Host "3. Run migrations: python -m alembic upgrade head" -ForegroundColor White
Write-Host "4. Start server: python -m uvicorn app.main:app --reload --port 8000" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop containers: docker-compose -f docker-compose.local.yml down" -ForegroundColor Yellow