# AgentOS Setup Guide

## Current Status

✅ **Completed**:
- Research and architecture design
- Comprehensive feature documentation
- Project structure creation
- Core backend implementation (FastAPI, models, services)
- Policy engine integration (OPA)
- Signal detection system
- Execution engine with tracing
- Tool gateway implementation
- Identity and credential management
- API endpoints (auth, agents, policies, executions)
- Frontend React dashboard structure
- Docker Compose configuration
- Database models and configuration
- Redis integration
- OpenTelemetry tracing setup
- Documentation (README, ARCHITECTURE, FEATURES)

⏳ **Remaining**:
- Action replay and rollback system
- Reliability testing and regression detection
- Budget management implementation
- Comprehensive testing suite
- Demo scenarios and examples
- GitHub repository setup and CI/CD
- Final validation and production hardening

## Quick Start

### 1. Install Prerequisites

Ensure you have:
- Docker Desktop installed and running
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- Git

### 2. Start with Docker Compose (Recommended)

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS\docker
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- OPA Policy Engine (port 8181)
- Jaeger Tracing (port 16686)
- AgentOS API (port 8000)
- AgentOS Dashboard (port 3000)

### 3. Access Services

- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Jaeger**: http://localhost:16686

### 4. Initialize Database

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS\backend
docker exec -it agentos-api alembic upgrade head
```

## Local Development Setup

### Backend

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS\backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your configuration
notepad .env

# Start infrastructure (PostgreSQL, Redis, OPA, Jaeger)
cd ..\docker
docker-compose up postgres redis opa jaeger -d

# Run migrations
cd ..\backend
alembic upgrade head

# Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## GitHub Setup

### Initialize Git Repository

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS
git init
git add .
git commit -m "Initial commit: AgentOS v0.1.0"
```

### Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `AgentOS`
3. Description: `The operating system for trustworthy AI agents`
4. Make it **Public** (for open source)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### Push to GitHub

```bash
# Add remote (replace with your username)
git remote add origin https://github.com/RaktimChandra/AgentOS.git

# Push main branch
git branch -M main
git push -u origin main
```

### Create GitHub Actions CI/CD

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: agentos
          POSTGRES_PASSWORD: agentos
          POSTGRES_DB: agentos
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/
```

## Testing the System

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

### 3. Create an Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-agent",
    "framework": "langchain",
    "trust_tier": 2,
    "description": "Test agent"
  }'
```

### 4. Execute Agent

```bash
curl -X POST http://localhost:8000/api/v1/executions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "AGENT_ID",
    "agent_token": "AGENT_TOKEN",
    "input_data": {"task": "test"}
  }'
```

## Next Steps

### Immediate (Required for Full Functionality)

1. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Set up database migrations**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

3. **Create alembic env file**:
   Create `backend/alembic/env.py` with proper database configuration

### Advanced Features (To Implement)

1. **Replay System**: Implement cut-point replay for regression testing
2. **Evaluation Pipeline**: Add L1 deterministic checks and L2 LLM-judge ensemble
3. **Budget Management**: Complete budget tracking and enforcement
4. **Testing Suite**: Add comprehensive unit and integration tests
5. **Demo Scenarios**: Create example agents and use cases

### Production Deployment

1. **Kubernetes manifests**: Create K8s deployment configs
2. **Secrets management**: Set up proper secret management
3. **Monitoring**: Configure Prometheus and Grafana
4. **Load balancing**: Set up ingress and load balancer
5. **Backup strategy**: Configure database backups

## Troubleshooting

### Frontend Lint Errors

The TypeScript errors in the frontend are expected until you run:
```bash
cd frontend
npm install
```

This will install all dependencies including React, React Router, Lucide icons, etc.

### Database Connection Issues

Ensure PostgreSQL is running:
```bash
docker-compose ps postgres
```

Check logs:
```bash
docker-compose logs postgres
```

### OPA Policy Engine

Check OPA is running:
```bash
curl http://localhost:8181/health
```

Load default policy:
```bash
curl -X PUT http://localhost:8181/v1/policies/agentos \
  -d @backend/policies/default.rego
```

## Architecture Overview

The system consists of:

1. **Backend (FastAPI)**: API server with policy engine, execution engine, and tool gateway
2. **Frontend (React)**: Dashboard for monitoring and control
3. **OPA**: Policy engine for runtime authorization
4. **PostgreSQL**: Persistent storage
5. **Redis**: Caching and session management
6. **Jaeger**: Distributed tracing

## Security Notes

- Change the `SECRET_KEY` in `.env` before production
- Use strong passwords for PostgreSQL and Redis
- Enable TLS/SSL for production
- Configure proper CORS origins
- Set up proper authentication for OPA

## Performance Tuning

- Adjust database pool sizes in config
- Configure Redis connection pooling
- Tune OPA decision caching
- Set appropriate timeout values
- Configure OpenTelemetry sampling

## Support

For issues or questions:
- Check the documentation in `docs/` folder
- Review the architecture in `ARCHITECTURE.md`
- See feature specifications in `FEATURES.md`
- Open an issue on GitHub

## License

MIT License - see LICENSE file
