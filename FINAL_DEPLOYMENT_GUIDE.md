# AgentOS - Final Deployment Guide

## 🎯 Quick Start Deployment

### Option 1: Automated Deployment (Recommended)

**Prerequisites**:
- Docker Desktop installed and running
- Windows PowerShell

**Steps**:
```powershell
# 1. Navigate to AgentOS directory
cd C:\Users\rakti\CascadeProjects\AgentOS

# 2. Run deployment script
.\deploy.ps1

# 3. Access services
# Dashboard: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Docker Deployment

```bash
# 1. Start Docker Desktop

# 2. Navigate to docker directory
cd C:\Users\rakti\CascadeProjects\AgentOS\docker

# 3. Start services
docker-compose up -d

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f

# 6. Stop services
docker-compose down
```

### Option 3: Manual Development Setup

**Backend Setup**:
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

# Start PostgreSQL and Redis (use Docker or install locally)
# Run migrations
alembic upgrade head

# Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Setup**:
```bash
cd C:\Users\rakti\CascadeProjects\AgentOS\frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Access at http://localhost:3000
```

## 🚀 GitHub Deployment

### Step 1: Create Repository

1. Go to https://github.com/new
2. Repository name: `AgentOS`
3. Description: `The operating system for trustworthy AI agents`
4. Make it **Public**
5. **Do not** initialize with README, .gitignore, or license
6. Click "Create repository"

### Step 2: Push to GitHub

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS

# Add remote
git remote add origin https://github.com/RaktimChandra/AgentOS.git

# Push to GitHub
git push -u origin main
```

### Step 3: Verify

Visit https://github.com/RaktimChandra/AgentOS to verify all files are present.

## 🧪 Testing

### Backend Tests

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS\backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v --cov=app
```

### Demo Examples

```bash
cd C:\Users\rakti\CascadeProjects\AgentOS

# Run demos (simulated output)
python examples/demo_agent.py
python examples/demo_replay.py
python examples/demo_evaluation.py
```

## 📊 Service Endpoints

### API Endpoints

- **Health**: `GET /health`
- **Auth**: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`
- **Agents**: `GET /api/v1/agents/`, `POST /api/v1/agents/`
- **Policies**: `GET /api/v1/policies/`, `POST /api/v1/policies/`
- **Executions**: `GET /api/v1/executions/`, `POST /api/v1/executions/`
- **Replays**: `GET /api/v1/replays/`, `POST /api/v1/replays/`
- **Evaluations**: `GET /api/v1/evaluations/`, `POST /api/v1/evaluations/`

### Dashboard Pages

- **Dashboard**: `/` - Overview and stats
- **Agents**: `/agents` - Agent management
- **Policies**: `/policies` - Policy management
- **Executions**: `/executions` - Execution history

## 🔧 Troubleshooting

### Docker Issues

**Problem**: Docker Desktop not running
**Solution**: Start Docker Desktop from Windows Start menu

**Problem**: Port already in use
**Solution**: Change port in docker-compose.yml or stop conflicting service

**Problem**: Services not starting
**Solution**: Check logs: `docker-compose logs <service>`

### Backend Issues

**Problem**: Module not found errors
**Solution**: Ensure virtual environment is activated and dependencies installed

**Problem**: Database connection error
**Solution**: Verify PostgreSQL is running and DATABASE_URL is correct

**Problem**: Redis connection error
**Solution**: Verify Redis is running and REDIS_URL is correct

### Frontend Issues

**Problem**: TypeScript errors
**Solution**: Run `npm install` to install dependencies

**Problem**: Build errors
**Solution**: Delete node_modules and package-lock.json, then run `npm install` again

## 📈 Monitoring

### Jaeger Tracing

Access Jaeger UI at http://localhost:16686 to view distributed traces.

### Prometheus Metrics

Metrics are exposed at `/metrics` endpoint on the API server.

### Logs

View logs with:
```bash
docker-compose logs -f api
docker-compose logs -f postgres
docker-compose logs -f redis
```

## 🔐 Security Configuration

### Before Production

1. **Change SECRET_KEY** in .env
   ```bash
   openssl rand -hex 32
   ```

2. **Change database passwords**
   - Update docker-compose.yml
   - Update .env file

3. **Configure CORS origins**
   - Update CORS_ORIGINS in .env

4. **Set up SSL/TLS**
   - Use reverse proxy (nginx)
   - Configure certificates

## 📝 Environment Variables

Required environment variables in .env:
- `SECRET_KEY` - JWT secret key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `OPA_URL` - OPA policy engine URL
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `ANTHROPIC_API_KEY` - Anthropic API key (optional)

## 🎯 Post-Deployment Checklist

- [ ] All services running
- [ ] API health check passing
- [ ] Dashboard accessible
- [ ] Database migrations applied
- [ ] OPA policy loaded
- [ ] Tracing working (Jaeger)
- [ ] Tests passing
- [ ] Logs being collected
- [ ] Monitoring configured
- [ ] Alerts configured

## 🏆 Success Criteria

Deployment is successful when:
- ✅ All Docker services are running
- ✅ API responds to health check
- ✅ Dashboard loads in browser
- ✅ API docs accessible
- ✅ Jaeger shows traces
- ✅ Can create user via API
- ✅ Can create agent via API
- ✅ Can execute agent via API

## 📞 Support

For issues:
1. Check VALIDATION_REPORT.md for known issues
2. Check DEPLOYMENT.md for detailed deployment guide
3. Check logs: `docker-compose logs`
4. Review documentation in docs/ folder

---

**Status**: ✅ DEPLOYMENT READY

**Date**: October 17, 2026

**Version**: 0.1.0
