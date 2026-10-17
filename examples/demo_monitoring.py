"""
Demo: Monitoring and Metrics

This example demonstrates the monitoring and metrics collection system.
"""

from app.monitoring.metrics import metrics_collector


def demo_monitoring():
    """Demo of monitoring system"""
    print("=== AgentOS Demo: Monitoring and Metrics ===\n")
    
    print("Prometheus Metrics:")
    print("  ✓ Agent execution counters and histograms")
    print("  ✓ Policy evaluation metrics")
    print("  ✓ Tool call metrics")
    print("  ✓ Signal detection metrics")
    print("  ✓ Budget utilization gauges")
    print("  ✓ Active agents/policies gauges")
    print("  ✓ System information")
    print()
    
    print("Metrics Collected:")
    print("""
    agent_executions_total
      - Total executions per agent
      - Labeled by agent_id and status
      
    agent_execution_duration_seconds
      - Execution duration histogram
      - Labeled by agent_id
      
    policy_evaluations_total
      - Total policy evaluations
      - Labeled by policy_id and decision
      
    tool_calls_total
      - Total tool calls
      - Labeled by tool_name and authorization status
      
    signal_detections_total
      - Total signal detections
      - Labeled by signal_type and severity
      
    budget_utilization_percent
      - Current budget utilization
      - Labeled by budget_id
    """)
    print()
    
    print("Example Usage:")
    print("""
    from app.monitoring.metrics import metrics_collector
    
    # Record agent execution
    metrics_collector.record_agent_execution(
        agent_id="agent-123",
        status="completed",
        duration=5.23,
    )
    
    # Record policy evaluation
    metrics_collector.record_policy_evaluation(
        policy_id="policy-123",
        decision="allow",
        duration=0.002,
    )
    
    # Record tool call
    metrics_collector.record_tool_call(
        tool_name="database",
        authorized=True,
        duration=0.15,
    )
    
    # Record signal detection
    metrics_collector.record_signal_detection(
        signal_type="sql_injection",
        severity="high",
    )
    
    # Update budget utilization
    metrics_collector.update_budget_utilization(
        budget_id="budget-123",
        utilization=75.5,
    )
    """)
    print()
    
    print("Accessing Metrics:")
    print("  • HTTP endpoint: /metrics")
    print("  • Prometheus format")
    print("  • Grafana dashboards")
    print("  • Alerting rules")
    print()
    
    print("Grafana Dashboard Examples:")
    print("  1. Agent Execution Rate")
    print("  2. Policy Decision Distribution")
    print("  3. Tool Call Authorization Rate")
    print("  4. Signal Detection Trends")
    print("  5. Budget Utilization Over Time")
    print("  6. Execution Duration Percentiles")
    print()
    
    print("Alerting Examples:")
    print("  • High execution failure rate")
    print("  • Policy denial spike")
    print("  • Budget utilization > 90%")
    print("  • Tool call latency > 1s")
    print("  • Signal detection spike")
    print()
    
    print("Demo Complete")
    print("This demonstrates:")
    print("  ✓ Prometheus metrics collection")
    print("  ✓ Execution tracking")
    print("  ✓ Policy evaluation metrics")
    print("  ✓ Tool call monitoring")
    print("  ✓ Signal detection tracking")
    print("  ✓ Budget monitoring")
    print("  ✓ Grafana dashboard integration")
    print("  ✓ Alerting capabilities")


if __name__ == "__main__":
    demo_monitoring()
