# AgentOS Examples

This directory contains example scripts demonstrating AgentOS capabilities.

## Examples

### demo_agent.py
Demonstrates a database query agent with policy enforcement.
- Runtime policy enforcement
- Trust tier-based authorization
- Signal detection (SQL injection)
- Execution tracing
- Budget management
- Audit logging

### demo_replay.py
Demonstrates the replay system for regression testing.
- Deterministic recording of executions
- Full replay (zero API calls)
- Cut-point replay (selective live testing)
- Regression detection
- Guarded boundary enforcement

### demo_evaluation.py
Demonstrates the evaluation pipeline.
- L1 deterministic checks (schema, PII, SQL guard, etc.)
- L2 LLM-judge ensemble (GPT-4, Claude, Gemini)
- Confidence-weighted aggregation
- Statistical quality gates
- Regression detection

## Running the Examples

```bash
# From the AgentOS root directory
python examples/demo_agent.py
python examples/demo_replay.py
python examples/demo_evaluation.py
```

## Note

These examples are simulations for demonstration purposes. In a real deployment, they would interact with actual databases, LLM APIs, and the full AgentOS system.
