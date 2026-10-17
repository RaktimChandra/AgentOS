# AgentOS API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except auth endpoints) require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

### Agents

#### Create Agent
```http
POST /agents/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "my-agent",
  "framework": "langchain",
  "trust_tier": 3,
  "description": "My AI agent"
}
```

#### List Agents
```http
GET /agents/
Authorization: Bearer <token>
```

#### Get Agent
```http
GET /agents/{agent_id}
Authorization: Bearer <token>
```

#### Generate Agent Credentials
```http
POST /agents/{agent_id}/credentials
Authorization: Bearer <token>
```

#### Delegate to Sub-Agent
```http
POST /agents/{agent_id}/delegate
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "sub-agent",
  "trust_tier": 2,
  "max_delegation_depth": 2
}
```

### Policies

#### Create Policy
```http
POST /policies/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "my-policy",
  "rego_code": "package auth\ndefault allow = true",
  "description": "My policy"
}
```

#### List Policies
```http
GET /policies/
Authorization: Bearer <token>
```

#### Get Policy
```http
GET /policies/{policy_id}
Authorization: Bearer <token>
```

#### Test Policy
```http
POST /policies/{policy_id}/test
Authorization: Bearer <token>
Content-Type: application/json

{
  "input": {...}
}
```

### Executions

#### Create Execution
```http
POST /executions/
Authorization: Bearer <token>
Content-Type: application/json

{
  "agent_id": "agent-123",
  "agent_token": "agent-token",
  "input_data": {"task": "analyze data"}
}
```

#### Get Execution
```http
GET /executions/{execution_id}
Authorization: Bearer <token>
```

#### Stream Execution
```http
GET /executions/{execution_id}/stream
Authorization: Bearer <token>
```

### Replays

#### Create Replay
```http
POST /replays/
Authorization: Bearer <token>
Content-Type: application/json

{
  "execution_id": "exec-123",
  "mode": "full",
  "cut_points": []
}
```

#### Get Replay
```http
GET /replays/{replay_id}
Authorization: Bearer <token>
```

#### Compare Replay
```http
POST /replays/{replay_id}/compare
Authorization: Bearer <token>
Content-Type: application/json

{
  "original_result": {...},
  "replay_result": {...}
}
```

### Evaluations

#### Create Evaluation
```http
POST /evaluations/
Authorization: Bearer <token>
Content-Type: application/json

{
  "execution_id": "exec-123",
  "output": {...},
  "checks_config": {...},
  "rubric": "Evaluate quality",
  "reference": "Reference output"
}
```

#### Regression Test
```http
POST /evaluations/regression
Authorization: Bearer <token>
Content-Type: application/json

{
  "baseline_execution_id": "exec-123",
  "new_execution_id": "exec-456",
  "baseline_output": {...},
  "new_output": {...},
  "checks_config": {...}
}
```

#### Batch Evaluation
```http
POST /evaluations/batch
Authorization: Bearer <token>
Content-Type: application/json

{
  "executions": [...],
  "checks_config": {...},
  "rubric": "Evaluate quality"
}
```

### Monitoring

#### Get Metrics
```http
GET /monitoring/metrics
Authorization: Bearer <token>
```

#### Health Check
```http
GET /monitoring/health
```

#### Get Stats
```http
GET /monitoring/stats
Authorization: Bearer <token>
```

### Webhooks

#### Create Webhook
```http
POST /webhooks/
Authorization: Bearer <token>
Content-Type: application/json

{
  "webhook_id": "webhook-123",
  "url": "https://example.com/webhook",
  "events": ["agent.execution.completed"],
  "secret": "webhook-secret"
}
```

#### List Webhooks
```http
GET /webhooks/
Authorization: Bearer <token>
```

#### Delete Webhook
```http
DELETE /webhooks/{webhook_id}
Authorization: Bearer <token>
```

#### Trigger Event
```http
POST /webhooks/trigger
Authorization: Bearer <token>
Content-Type: application/json

{
  "event_type": "agent.execution.completed",
  "payload": {...}
}
```

### Audit

#### Get Audit Logs
```http
GET /audit/
Authorization: Bearer <token>
Query Parameters:
  - actor_id (optional)
  - resource_id (optional)
  - action (optional)
  - limit (default: 100)
```

#### Get Agent Audit Trail
```http
GET /audit/agent/{agent_id}
Authorization: Bearer <token>
```

#### Get Resource History
```http
GET /audit/resource/{resource_type}/{resource_id}
Authorization: Bearer <token>
```

### Analytics

#### Get Overview
```http
GET /analytics/overview
Authorization: Bearer <token>
```

#### Get Execution Trend
```http
GET /analytics/executions/trend
Authorization: Bearer <token>
Query Parameters:
  - days (default: 30)
```

#### Get Policy Decision Distribution
```http
GET /analytics/policy/decisions
Authorization: Bearer <token>
```

#### Get Tool Usage Stats
```http
GET /analytics/tools/usage
Authorization: Bearer <token>
```

#### Get Signal Distribution
```http
GET /analytics/signals/distribution
Authorization: Bearer <token>
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

All authenticated endpoints are rate limited to:
- 100 requests per minute per user
- 1000 requests per hour per user

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1634567890
```

## Pagination

List endpoints support pagination via query parameters:
```
?page=1&limit=50
```

Response includes pagination metadata:
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "limit": 50,
  "pages": 3
}
```
