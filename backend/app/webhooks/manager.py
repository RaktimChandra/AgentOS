"""Webhook system for event notifications"""

import hmac
import hashlib
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio


class WebhookManager:
    """Manager for webhook delivery"""
    
    def __init__(self):
        self.webhooks: Dict[str, Dict[str, Any]] = {}
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def register_webhook(
        self,
        webhook_id: str,
        url: str,
        events: List[str],
        secret: str,
    ) -> bool:
        """
        Register a webhook
        
        Args:
            webhook_id: Webhook identifier
            url: Webhook URL
            events: List of events to subscribe to
            secret: Secret for signature verification
            
        Returns:
            True if successful
        """
        self.webhooks[webhook_id] = {
            "url": url,
            "events": events,
            "secret": secret,
            "created_at": datetime.utcnow().isoformat(),
            "delivery_count": 0,
            "last_delivery": None,
        }
        return True
    
    async def unregister_webhook(self, webhook_id: str) -> bool:
        """
        Unregister a webhook
        
        Args:
            webhook_id: Webhook identifier
            
        Returns:
            True if successful
        """
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            return True
        return False
    
    async def trigger_event(
        self,
        event_type: str,
        payload: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Trigger an event to all registered webhooks
        
        Args:
            event_type: Event type
            payload: Event payload
            
        Returns:
            List of delivery results
        """
        results = []
        
        for webhook_id, webhook in self.webhooks.items():
            if event_type in webhook["events"]:
                result = await self._deliver_webhook(
                    webhook_id=webhook_id,
                    webhook=webhook,
                    event_type=event_type,
                    payload=payload,
                )
                results.append(result)
        
        return results
    
    async def _deliver_webhook(
        self,
        webhook_id: str,
        webhook: Dict[str, Any],
        event_type: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Deliver webhook to URL
        
        Args:
            webhook_id: Webhook identifier
            webhook: Webhook configuration
            event_type: Event type
            payload: Event payload
            
        Returns:
            Delivery result
        """
        # Prepare payload
        webhook_payload = {
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": payload,
        }
        
        # Generate signature
        signature = self._generate_signature(
            webhook["secret"],
            webhook_payload,
        )
        
        # Send webhook
        try:
            response = await self.client.post(
                webhook["url"],
                json=webhook_payload,
                headers={
                    "X-AgentOS-Signature": signature,
                    "X-AgentOS-Event": event_type,
                    "Content-Type": "application/json",
                },
            )
            
            # Update webhook stats
            webhook["delivery_count"] += 1
            webhook["last_delivery"] = datetime.utcnow().isoformat()
            
            return {
                "webhook_id": webhook_id,
                "status": "success",
                "status_code": response.status_code,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            return {
                "webhook_id": webhook_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
    
    def _generate_signature(
        self,
        secret: str,
        payload: Dict[str, Any],
    ) -> str:
        """
        Generate HMAC signature
        
        Args:
            secret: Secret key
            payload: Payload to sign
            
        Returns:
            Signature
        """
        import json
        payload_str = json.dumps(payload, separators=(",", ":"))
        signature = hmac.new(
            secret.encode(),
            payload_str.encode(),
            hashlib.sha256,
        ).hexdigest()
        return f"sha256={signature}"
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global webhook manager instance
webhook_manager = WebhookManager()
