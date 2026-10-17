"""Webhook endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any
from app.core.security import get_current_user_id
from app.webhooks.manager import webhook_manager

router = APIRouter()


class WebhookCreate(BaseModel):
    """Webhook creation request"""
    webhook_id: str
    url: str
    events: List[str]
    secret: str


class WebhookResponse(BaseModel):
    """Webhook response"""
    webhook_id: str
    url: str
    events: List[str]
    created_at: str
    delivery_count: int
    last_delivery: str


@router.post("/")
async def create_webhook(
    webhook_data: WebhookCreate,
    user_id: str = Depends(get_current_user_id),
):
    """Create a new webhook"""
    success = await webhook_manager.register_webhook(
        webhook_id=webhook_data.webhook_id,
        url=webhook_data.url,
        events=webhook_data.events,
        secret=webhook_data.secret,
    )
    
    if success:
        return {"status": "created", "webhook_id": webhook_data.webhook_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create webhook",
        )


@router.get("/")
async def list_webhooks(user_id: str = Depends(get_current_user_id)):
    """List all webhooks"""
    return {"webhooks": list(webhook_manager.webhooks.values())}


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Delete a webhook"""
    success = await webhook_manager.unregister_webhook(webhook_id)
    
    if success:
        return {"status": "deleted", "webhook_id": webhook_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )


@router.post("/trigger")
async def trigger_event(
    event_type: str,
    payload: Dict[str, Any],
    user_id: str = Depends(get_current_user_id),
):
    """Trigger an event to all webhooks"""
    results = await webhook_manager.trigger_event(event_type, payload)
    return {"results": results}
