# AgentOS Deployment Script
# Run this script to deploy AgentOS locally

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AgentOS Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker Desktop status..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker is installed: $dockerVersion" -ForegroundColor Green
    
    $dockerPs = docker ps
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Desktop is not running" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please start Docker Desktop and run this script again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative: Manual deployment without Docker" -ForegroundColor Cyan
    Write-Host "1. Install PostgreSQL and Redis manually" -ForegroundColor White
    Write-Host "2. Install Python dependencies: cd backend && pip install -r requirements.txt" -ForegroundColor White
    Write-Host "3. Install frontend dependencies: cd frontend && npm install" -ForegroundColor White
    Write-Host "4. Configure .env file" -ForegroundColor White
    Write-Host "5. Run backend: uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host "6. Run frontend: npm run dev" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "Starting AgentOS deployment..." -ForegroundColor Cyan
Write-Host ""

# Navigate to docker directory
Set-Location docker

# Start all services
Write-Host "Starting Docker Compose services..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Services started successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to start services" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host ""
Write-Host "Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access AgentOS at:" -ForegroundColor Cyan
Write-Host "  Dashboard: http://localhost:3000" -ForegroundColor White
Write-Host "  API: http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Jaeger: http://localhost:16686" -ForegroundColor White
Write-Host "  OPA: http://localhost:8181" -ForegroundColor White
Write-Host ""
Write-Host "To stop services:" -ForegroundColor Yellow
Write-Host "  cd docker && docker-compose down" -ForegroundColor White
Write-Host ""
