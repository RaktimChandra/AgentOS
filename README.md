# AgentOS

**The Operating System for Trustworthy AI Agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org)

AgentOS is a production-grade platform where companies can deploy AI agents with permission boundaries, execution traces, budgets, rollback capabilities, and measurable reliability.

## 🚀 Features

### Core Capabilities

- **Verifiable Agent Identity**: JWT-based credentials with delegation chains and trust tiers
- **Runtime Policy Enforcement**: OPA-based policy engine with 150+ signal detection
- **Tool Gateway**: Intercept and authorize all tool calls with guardrails
- **Execution Tracing**: OpenTelemetry-native observability for every agent decision
- **Replay System**: Deterministic record/replay for regression testing
- **Budget Management**: Cost caps, rate limits, and resource controls
- **Evaluation Pipeline**: L1 deterministic checks + L2 LLM-judge ensemble
- **Dashboard UI**: React-based monitoring and control plane

### Security Features

- Agent-shaped credentials with DPoP binding
- Just-in-time credential brokering (no standing secrets)
- Cascade revocation (revoke parent, entire tree collapses)
- Intent drift detection
- PII/secret detection and redaction
- SQL/command injection detection
- Prompt injection detection

### Innovation Highlights

- **Cut-Point Replay**: Selective live testing from recorded incidents
- **150+ Signal Detection**: Most comprehensive runtime signal collection
- **Statistical Quality Gates**: Paired-bootstrap significance for regression detection
- **Zero Standing Secrets**: JIT credential brokering eliminates credential leakage
- **Byte-Identical Replay**: 100% determinism enables reliable regression testing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AgentOS Dashboard                        │
│                    (React + TypeScript + Tailwind)              │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTPS/WebSocket
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway (FastAPI)                       │
│  • Authentication (JWT/OAuth)                                    │
│  • Rate Limiting                                                  │
│  • Request Validation                                            │
└─────────────────┬───────────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌─────────┐   ┌──────────┐   ┌──────────────┐
│ Policy  │   │ Execution│   │   Storage    │
│ Engine  │   │ Engine   │   │   Layer      │
│  (OPA)  │   │          │   │              │
└─────────┘   └──────────┘   └──────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Policy Engine**: Open Policy Agent (OPA)
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Tracing**: OpenTelemetry
- **Testing**: pytest

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **Components**: shadcn/ui
- **State**: React Query + Zustand

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose (dev), Kubernetes (prod)
- **Monitoring**: Jaeger, Prometheus
- **Policy**: OPA

## 📦 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- OpenAI API key (optional, for LLM features)
- Anthropic API key (optional, for LLM features)

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/RaktimChandra/AgentOS.git
cd AgentOS
```

2. Start all services:
```bash
cd docker
docker-compose up -d
```

3. Access the services:
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Jaeger Tracing**: http://localhost:16686
- **OPA**: http://localhost:8181

### Local Development

#### Backend

1. Install dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start PostgreSQL, Redis, and OPA (using Docker):
```bash
cd docker
docker-compose up postgres redis opa jaeger -d
```

4. Run database migrations:
```bash
cd backend
alembic upgrade head
```

5. Start the API server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Access the dashboard at http://localhost:3000

## 📖 Usage

### Creating an Agent

```python
from app.identity.service import IdentityService
from app.models.agent import AgentFramework

identity_service = IdentityService(db)

agent = await identity_service.create_agent(
    owner_id="user-123",
    name="data-analyzer",
    framework=AgentFramework.LANGCHAIN,
    trust_tier=3,
    max_delegation_depth=3,
)

# Get agent credentials
token = await identity_service.create_agent_credentials(agent)
```

### Executing an Agent with LLM

```python
from app.execution.engine import ExecutionEngine
from app.integrations.openai import openai_integration

execution_engine = ExecutionEngine(db)

# Use LLM for agent reasoning
llm_response = await openai_integration.chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Analyze this data"},
    ],
    model="gpt-4",
)

result = await execution_engine.execute_agent(
    agent_id="agent-123",
    agent_token=agent_token,
    input_data={"task": "analyze data"},
    timeout=300,
)
```

### Creating a Policy

```rego
package agentos.auth

default allow = false

allow {
    input.agent.trust_tier >= input.tool.min_trust_tier
    input.action in input.agent.allowed_actions
    not high_risk_signals
    within_budget
}
```

### Setting Up Webhooks

```python
from app.webhooks.manager import webhook_manager

await webhook_manager.register_webhook(
    webhook_id="webhook-123",
    url="https://example.com/webhook",
    events=["agent.execution.completed", "policy.denied"],
    secret="your-secret-key",
)
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Demo Examples

```bash
# Run demo scripts
python examples/demo_agent.py
python examples/demo_replay.py
python examples/demo_evaluation.py
python examples/demo_llm_integration.py
python examples/demo_monitoring.py
python examples/demo_webhooks.py
```

## 📊 Monitoring

### Jaeger Tracing

Access Jaeger UI at http://localhost:16686 to view distributed traces.

### Metrics

Prometheus metrics are exposed at `/metrics` endpoint.

## 🔐 Security

- All credentials are JWT-based with DPoP binding
- Secrets are never exposed to agents (JIT credential brokering)
- All tool calls are intercepted and authorized
- Comprehensive signal detection for security threats
- Immutable audit trail for compliance

## 📝 Documentation

- [Architecture](ARCHITECTURE.md) - Detailed system architecture
- [Features](FEATURES.md) - Complete feature specifications
- [API Reference](docs/API_REFERENCE.md) - Complete API documentation
- [Contributing](docs/CONTRIBUTING.md) - Contribution guidelines
- [Roadmap](docs/ROADMAP.md) - Future development plans
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## 🌟 Star History

If you find AgentOS useful, please consider giving it a star on GitHub!

## 📧 Contact

- **Author**: Raktim Chandra
- **GitHub**: [@RaktimChandra](https://github.com/RaktimChandra)

## 🙏 Acknowledgments

Inspired by and incorporating best practices from:
- [Noma](https://noma.security/) - Agent access control
- [Oleria](https://www.oleria.com/) - Zero trust for agents
- [Highflame](https://www.highflame.com/) - Agent identity and authorization
- [TraceGym](https://github.com/hoomanesteki/tracegym-ai-agent-evaluation) - Replay and evaluation
- [Chronicle](https://github.com/theagentplane/chronicle) - Cut-point replay
- [EvalView](https://evalview.com/) - Regression testing
