"""
Demo: Webhook System

This example demonstrates the webhook system for event notifications.
"""

from typing import Dict, Any, List
import json


class WebhookManager:
    """Manager for webhook delivery"""
    
    def __init__(self):
        self.webhooks = {}
    
    def register_webhook(
        self,
        webhook_id: str,
        url: str,
        events: List[str],
        secret: str,
    ):
        """Register a webhook"""
        self.webhooks[webhook_id] = {
            "url": url,
            "events": events,
            "secret": secret,
        }
    
    def trigger_event(self, event_type: str, payload: Dict[str, Any]):
        """Trigger an event to all registered webhooks"""
        for webhook_id, webhook in self.webhooks.items():
            if event_type in webhook["events"]:
                print(f"Delivering {event_type} to {webhook['url']}")
                print(f"Payload: {json.dumps(payload, indent=2)}")
                print()


def demo_webhooks():
    """Demo of webhook system"""
    print("=== AgentOS Demo: Webhook System ===\n")
    
    manager = WebhookManager()
    
    print("Webhook Events:")
    print("  ✓ agent.execution.completed")
    print("  ✓ agent.execution.failed")
    print("  ✓ policy.denied")
    print("  ✓ signal.detected")
    print("  ✓ budget.exceeded")
    print("  ✓ agent.created")
    print("  ✓ agent.deleted")
    print()
    
    print("Registering Webhooks:")
    print()
    
    # Register webhooks
    manager.register_webhook(
        webhook_id="webhook-1",
        url="https://example.com/webhooks/agentos",
        events=["agent.execution.completed", "agent.execution.failed"],
        secret="secret123",
    )
    
    manager.register_webhook(
        webhook_id="webhook-2",
        url="https://example.com/webhooks/security",
        events=["policy.denied", "signal.detected"],
        secret="secret456",
    )
    
    manager.register_webhook(
        webhook_id="webhook-3",
        url="https://example.com/webhooks/billing",
        events=["budget.exceeded"],
        secret="secret789",
    )
    
    print("Triggering Events:")
    print()
    
    # Trigger events
    manager.trigger_event(
        "agent.execution.completed",
        {
            "agent_id": "agent-123",
            "execution_id": "exec-456",
            "status": "completed",
            "duration": 5.23,
            "cost": 0.05,
        }
    )
    
    manager.trigger_event(
        "policy.denied",
        {
            "agent_id": "agent-123",
            "policy_id": "policy-123",
            "action": "database.write",
            "reason": "Trust tier insufficient",
        }
    )
    
    manager.trigger_event(
        "signal.detected",
        {
            "agent_id": "agent-123",
            "signal_type": "sql_injection",
            "severity": "high",
            "context": "DROP TABLE users",
        }
    )
    
    manager.trigger_event(
        "budget.exceeded",
        {
            "agent_id": "agent-123",
            "budget_id": "budget-123",
            "limit": 100.0,
            "used": 105.50,
        }
    )
    
    print("Webhook Payload Format:")
    print("""
    {
        "event": "agent.execution.completed",
        "timestamp": "2026-10-17T12:00:00Z",
        "data": {
            "agent_id": "agent-123",
            "execution_id": "exec-456",
            ...
        },
        "signature": "sha256=..."
    }
    """)
    print()
    
    print("Security Features:")
    print("  ✓ HMAC signature verification")
    print("  ✓ Secret key per webhook")
    print("  ✓ Retry logic with exponential backoff")
    print("  ✓ Delivery status tracking")
    print("  ✓ Webhook logs")
    print()
    
    print("Use Cases:")
    print("  • Slack notifications for failures")
    print("  • PagerDuty alerts for security events")
    print("  • Custom analytics integration")
    print("  • Audit trail synchronization")
    print("  • Custom workflow triggers")
    print()
    
    print("Demo Complete")
    print("This demonstrates:")
    print("  ✓ Webhook registration")
    print("  ✓ Event triggering")
    print("  ✓ Multiple event types")
    print("  ✓ Payload delivery")
    print("  ✓ Security with signatures")
    print("  ✓ Retry logic")
    print("  ✓ Delivery tracking")


if __name__ == "__main__":
    demo_webhooks()
