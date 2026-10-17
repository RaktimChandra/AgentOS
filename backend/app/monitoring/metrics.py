"""Metrics collection and reporting"""

from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client import start_http_server
from typing import Optional
from app.core.config import get_settings

settings = get_settings()

# Metrics
agent_executions_total = Counter(
    'agent_executions_total',
    'Total number of agent executions',
    ['agent_id', 'status']
)

agent_execution_duration = Histogram(
    'agent_execution_duration_seconds',
    'Agent execution duration in seconds',
    ['agent_id']
)

policy_evaluations_total = Counter(
    'policy_evaluations_total',
    'Total number of policy evaluations',
    ['policy_id', 'decision']
)

policy_evaluation_duration = Histogram(
    'policy_evaluation_duration_seconds',
    'Policy evaluation duration in seconds',
    ['policy_id']
)

tool_calls_total = Counter(
    'tool_calls_total',
    'Total number of tool calls',
    ['tool_name', 'authorized']
)

tool_call_duration = Histogram(
    'tool_call_duration_seconds',
    'Tool call duration in seconds',
    ['tool_name']
)

signal_detections_total = Counter(
    'signal_detections_total',
    'Total number of signal detections',
    ['signal_type', 'severity']
)

budget_utilization = Gauge(
    'budget_utilization_percent',
    'Budget utilization percentage',
    ['budget_id']
)

active_agents = Gauge(
    'active_agents',
    'Number of active agents'
)

active_policies = Gauge(
    'active_policies',
    'Number of active policies'
)

system_info = Info(
    'agentos_info',
    'AgentOS system information'
)


class MetricsCollector:
    """Collect and report system metrics"""
    
    def __init__(self, port: Optional[int] = None):
        self.port = port or settings.METRICS_PORT
        self.server_started = False
    
    async def start_server(self):
        """Start Prometheus metrics server"""
        if not self.server_started:
            start_http_server(self.port)
            self.server_started = True
            
            # Set system info
            system_info.info({
                'version': '0.1.0',
                'environment': settings.ENVIRONMENT,
            })
    
    def record_agent_execution(self, agent_id: str, status: str, duration: float):
        """Record agent execution metrics"""
        agent_executions_total.labels(agent_id=agent_id, status=status).inc()
        agent_execution_duration.labels(agent_id=agent_id).observe(duration)
    
    def record_policy_evaluation(self, policy_id: str, decision: str, duration: float):
        """Record policy evaluation metrics"""
        policy_evaluations_total.labels(policy_id=policy_id, decision=decision).inc()
        policy_evaluation_duration.labels(policy_id=policy_id).observe(duration)
    
    def record_tool_call(self, tool_name: str, authorized: bool, duration: float):
        """Record tool call metrics"""
        tool_calls_total.labels(tool_name=tool_name, authorized=str(authorized)).inc()
        tool_call_duration.labels(tool_name=tool_name).observe(duration)
    
    def record_signal_detection(self, signal_type: str, severity: str):
        """Record signal detection metrics"""
        signal_detections_total.labels(signal_type=signal_type, severity=severity).inc()
    
    def update_budget_utilization(self, budget_id: str, utilization: float):
        """Update budget utilization gauge"""
        budget_utilization.labels(budget_id=budget_id).set(utilization)
    
    def update_active_agents(self, count: int):
        """Update active agents gauge"""
        active_agents.set(count)
    
    def update_active_policies(self, count: int):
        """Update active policies gauge"""
        active_policies.set(count)


# Global metrics collector instance
metrics_collector = MetricsCollector()
