# AgentOS Architecture

## Vision

AgentOS is the operating system for trustworthy AI agents - a production-grade platform where companies can deploy AI agents with permission boundaries, execution traces, budgets, rollback capabilities, and measurable reliability.

## Core Philosophy

**Treat every agent like production infrastructure**

- Agents have verifiable identities, not shared API keys
- Every action is authorized at runtime against policy
- All executions are recorded and replayable for testing
- Budgets cap costs before they explode
- Regressions are detected automatically in CI
- Rollback is instant when something breaks

## Architecture Overview

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
│  • API Versioning                                                │
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
    │               │               │
    │         ┌─────┴─────┐         │
    │         │           │         │
    ▼         ▼           ▼         ▼
┌─────────┐ ┌─────┐   ┌──────┐  ┌─────────┐
│Replay   │ │Tool │   │Trace │  │PostgreSQL│
│System   │ │Gate │   │Layer │  │  Redis   │
└─────────┘ └─────┘   └──────┘  └─────────┘
                    │
                    ▼
            ┌───────────────┐
            │  External     │
            │  Services    │
            │  (APIs, DBs) │
            └───────────────┘
```

## System Components

### 1. Identity Layer

**Purpose**: Provide verifiable, agent-shaped credentials with delegation chains

**Features**:
- Agent credentials carrying: owner, trust tier, framework, delegation depth
- Delegation chain tracking (human → agent → sub-agent)
- Scope attenuation at every hop
- Just-in-time, ephemeral credentials (no standing access)
- Cascade revocation (revoke parent, entire tree collapses)
- Human-anchored identity (offboard human, revoke all agents)

**Implementation**:
- JWT-based credentials with DPoP (Demonstration of Proof-of-Possession)
- SPIFFE/WIMSE-compliant identity format
- Credential binding to proof keys (stolen tokens are inert)
- OAuth 2.1 and RFC 8693 token exchange

### 2. Policy Engine (OPA)

**Purpose**: Runtime authorization with 150+ live signals

**Features**:
- Policy-as-code with Rego language
- One Cedar policy enforced across all boundaries
- 30+ prebuilt detectors emitting typed signals:
  - Prompt injection detection
  - Tool poisoning detection
  - PII/secret detection
  - Runaway loop detection
  - Intent drift detection
- Adaptive guardrails with breakout controls
- Out-of-band enforcement (engine denies unless policy permits)
- Fail-open vs fail-closed per surface

**Policy Categories**:
- **Tool Authorization**: Which tools can an agent use?
- **Action Authorization**: Which specific operations within tools?
- **Data Authorization**: What data can be accessed?
- **Context-Aware Controls**: Based on user, task, risk level
- **Budget Controls**: Rate limits, cost caps, time windows

**Example Policy**:
```rego
package agentos.auth

default allow = false

allow {
    # Check agent identity
    input.agent.trust_tier >= input.tool.min_trust_tier
    
    # Check delegation depth
    input.agent.delegation_depth <= input.tool.max_delegation
    
    # Check action permissions
    input.action in input.agent.allowed_actions
    
    # No intent drift
    not intent_drift
    
    # Within budget
    within_budget
}

intent_drift {
    input.detected_intent != input.stated_intent
    input.detected_intent.risk_level == "high"
}

within_budget {
    input.agent.cost_used < input.agent.budget_limit
}
```

### 3. Execution Engine

**Purpose**: Sandboxed runtime for agent execution with tool gateways

**Features**:
- Per-call isolation with microVM containment
- Tool gateway intercepting all external calls
- Credential brokering (secrets never reach agent)
- Execution timeout enforcement
- Resource limits (CPU, memory, network)
- Deterministic execution for replay

**Tool Gateway**:
- MCP (Model Context Protocol) server support
- REST API proxy with argument validation
- Database query guardrails (SQL AST analysis)
- File system sandboxing
- HTTP request filtering
- Shell command whitelisting

**Execution Flow**:
1. Agent requests tool call
2. Gateway validates against policy
3. If approved, broker credentials JIT
4. Execute with timeout and limits
5. Capture full trace (input, output, timing)
6. Return result to agent

### 4. Tracing Layer (OpenTelemetry)

**Purpose**: Complete observability of every agent decision

**Features**:
- OpenTelemetry GenAI semantic conventions
- Span hierarchy: agent → tool → external service
- Capture: prompts, responses, tool calls, errors, latency
- Cost attribution per agent/team
- Context propagation across boundaries
- Export to multiple backends (Jaeger, Prometheus, custom)

**Span Attributes**:
- `gen_ai.system.name`: Agent framework
- `gen_ai.request.model`: LLM used
- `gen_ai.request.prompt_tokens`: Input token count
- `gen_ai.response.completion_tokens`: Output token count
- `gen_ai.tool.name`: Tool called
- `gen_ai.tool.parameters`: Tool arguments (redacted)
- `agent.id`: Agent identity
- `agent.owner`: Human owner
- `agent.delegation_chain`: Full chain
- `policy.decision`: Allow/deny/approve
- `policy.reason`: Policy explanation

### 5. Replay System

**Purpose**: Deterministic replay for testing and regression detection

**Features**:
- **Full Replay**: All boundaries from record, zero API calls
- **Cut-Point Replay**: Selected boundaries live, rest from record
- Byte-identical reproducibility (100% determinism)
- Guarded boundary call-count checks
- Mutation testing support
- CI integration with quality gates

**Recording Strategy**:
- Record at non-deterministic boundaries:
  - LLM calls (model responses)
  - Tool calls (external service responses)
  - Database queries (state reads)
- Store as content-addressed fixtures
- Compress with zstd
- SQLite for metadata, blobs for payloads

**Cut-Point Testing**:
1. Record incident with all boundaries
2. Choose which boundaries to test live (e.g., tool gate)
3. Replay with live code at cut-points
4. Stub remaining boundaries from record
5. Detect if fix prevents unsafe action
6. Accept benign changes

### 6. Budget Manager

**Purpose**: Cost controls and resource limits

**Features**:
- Per-agent budget caps
- Team-level budget pooling
- Rate limiting per tool/model
- Cost attribution and reporting
- Predictive cost estimation
- Automatic budget alerts
- Emergency shutoff

**Budget Types**:
- **Token Budget**: Max tokens per time window
- **API Call Budget**: Max calls per tool
- **Monetary Budget**: Max spend in USD
- **Time Budget**: Max execution duration
- **Resource Budget**: CPU/memory limits

**Enforcement**:
- Pre-execution budget check
- Real-time cost tracking
- Mid-execution termination on overage
- Budget rollover configuration
- Emergency override with approval

### 7. Evaluation Pipeline

**Purpose**: Automated reliability testing and regression detection

**Features**:
- **L1 Deterministic Checks**:
  - Schema validation
  - Citation/grounding checks
  - SQL AST guard
  - SQL execution accuracy oracle
  - Tool-selection correctness
  - Trajectory validity
  - PII detection
  - Cost/latency budgets
  
- **L2 LLM-Judge Ensemble**:
  - Cross-family judge ensemble (GPT, Claude, Gemini)
  - Cached by (case, output, rubric, model)
  - Confidence reporting
  - NEEDS_REVIEW when judges disagree
  - Calibrated scoring ladder

- **Statistical Rigor**:
  - Paired-bootstrap significance testing
  - Exact sign test for pass/fail flips
  - Cohen's κ for inter-rater agreement
  - 95% confidence intervals

**Quality Gates**:
- Block on: new invariant failure, mean score drop (CI < 0), cost regression
- Warn on: uncertain wobbles, judge disagreement
- Pass on: all checks green

### 8. Dashboard UI

**Purpose**: Monitoring and control plane

**Features**:
- Real-time agent monitoring
- Policy editor with Rego syntax highlighting
- Trace viewer with span hierarchy
- Budget dashboard with cost attribution
- Replay test runner with diff viewer
- Alert management
- Agent lifecycle management
- User/team management

**UI Stack**:
- React 18 with TypeScript
- TailwindCSS for styling
- shadcn/ui components
- Lucide icons
- Recharts for visualizations
- React Query for data fetching
- WebSocket for real-time updates

### 9. API Gateway (FastAPI)

**Purpose**: RESTful API with authentication and validation

**Features**:
- JWT authentication
- OAuth 2.0 integration
- API key management
- Rate limiting (per user, per agent)
- Request validation with Pydantic
- OpenAPI documentation
- CORS configuration
- WebSocket support for real-time streams

**API Endpoints**:
- `/agents/` - CRUD for agents
- `/policies/` - Policy management
- `/executions/` - Execution management
- `/traces/` - Trace querying
- `/replays/` - Replay operations
- `/budgets/` - Budget management
- `/evaluations/` - Evaluation runs
- `/users/` - User management

### 10. Storage Layer

**Purpose**: Persistent storage and caching

**PostgreSQL Schema**:
- `agents` - Agent definitions and credentials
- `policies` - Policy rules and versions
- `executions` - Execution records
- `traces` - Trace spans (time-series optimized)
- `replays` - Replay fixtures and results
- `budgets` - Budget allocations and usage
- `users` - User accounts and permissions
- `audit_log` - Complete audit trail

**Redis Usage**:
- Session caching
- Rate limit counters
- Real-time metrics
- Pub/sub for events
- Credential caching (TTL-based)

## Security Model

### Defense in Depth

1. **Identity**: Verifiable credentials with delegation chains
2. **Authentication**: JWT + DPoP proof keys
3. **Authorization**: OPA policy at every boundary
4. **Containment**: microVM isolation per execution
5. **Credential Brokering**: No standing secrets
6. **Monitoring**: Full trace capture
7. **Audit**: Immutable audit log
8. **Testing**: Automated regression detection

### Threat Mitigations

- **Prompt Injection**: Detector in policy engine + input sanitization
- **Tool Poisoning**: MCP server validation + signature verification
- **Credential Theft**: DPoP binding + JIT credential brokering
- **Runaway Loops**: Step limits + cost caps + timeout enforcement
- **Data Exfiltration**: PII detection + output filtering
- **Privilege Escalation**: Scope attenuation + delegation depth limits
- **Supply Chain Attacks**: Signed policies + dependency pinning

## Deployment Architecture

### Docker Compose (Development)

```
agentos-api          (FastAPI)
agentos-dashboard    (React)
agentos-worker       (Celery)
agentos-opa          (OPA server)
agentos-jaeger       (Tracing)
agentos-postgres     (PostgreSQL)
agentos-redis        (Redis)
```

### Kubernetes (Production)

- Horizontal Pod Autoscaling
- Pod Disruption Budgets
- Network policies
- Secrets management (External Secrets Operator)
- Ingress with TLS
- Persistent volumes for PostgreSQL

## Technology Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Policy Engine**: Open Policy Agent (OPA)
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Tracing**: OpenTelemetry
- **Testing**: pytest + pytest-asyncio

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **Components**: shadcn/ui
- **State**: React Query + Zustand
- **Charts**: Recharts

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes (production)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: Loki
- **Tracing**: Jaeger

## Innovation Highlights

1. **Cut-Point Replay**: First to enable selective live testing from recorded incidents
2. **Agent-Shaped Credentials**: Verifiable identity designed for agents, not humans
3. **150+ Signal Detection**: Most comprehensive runtime signal collection
4. **Statistical Quality Gates**: Paired-bootstrap significance for regression detection
5. **Cascade Revocation**: Instant revocation across entire delegation trees
6. **Zero Standing Secrets**: JIT credential brokering eliminates credential leakage
7. **Byte-Identical Replay**: 100% determinism enables reliable regression testing
8. **Multi-Judge Ensemble**: Calibrated LLM evaluation with confidence reporting

## Performance Targets

- Policy evaluation latency: < 10ms (p95)
- Tool gateway overhead: < 5ms (p95)
- Full replay speed: 100x faster than live execution
- Trace ingestion: > 10,000 spans/sec
- API response time: < 100ms (p95)
- Dashboard load time: < 2s

## Scalability

- Horizontal scaling of API and worker nodes
- Database sharding for traces (time-based)
- Redis clustering for cache
- OPA decision caching
- Connection pooling for databases
- Async I/O throughout

## Reliability

- 99.9% uptime SLA
- Automated failover
- Database replication
- Backup every 5 minutes
- Point-in-time recovery
- Circuit breakers for external services
- Rate limiting to prevent cascading failures

## Compliance

- SOC 2 Type II ready
- GDPR compliant (data residency, right to deletion)
- EU AI Act compliant (August 2026 deadline)
- Audit trail retention: 7 years
- Data encryption at rest and in transit
- Regular penetration testing

## Roadmap

### Phase 1: Core Platform (MVP)
- Identity layer with basic credentials
- OPA policy engine
- Execution engine with tool gateway
- Basic tracing
- Simple budget controls
- FastAPI backend
- React dashboard

### Phase 2: Testing & Reliability
- Replay system (full replay)
- Evaluation pipeline (L1 checks)
- Regression detection
- CI/CD integration

### Phase 3: Advanced Features
- Cut-point replay
- L2 LLM-judge ensemble
- Advanced detectors (30+)
- Cascade revocation
- JIT credential brokering

### Phase 4: Enterprise
- Multi-tenant support
- SSO integration
- Advanced RBAC
- Compliance reporting
- Enterprise SLAs
- Premium support

## Open Source Strategy

- Core platform: MIT license
- Enterprise features: Commercial license
- Community contributions encouraged
- Security bounty program
- Regular releases (monthly)
- Long-term support (LTS) versions
