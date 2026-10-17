"""Audit log endpoints"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.audit.service import get_audit_service
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class AuditLogResponse(BaseModel):
    """Audit log response"""
    id: str
    actor_type: str
    actor_id: str
    action: str
    resource_type: str
    resource_id: str
    details: dict
    policy_decision: Optional[str]
    timestamp: datetime


@router.get("/")
async def get_audit_logs(
    actor_id: Optional[str] = Query(None),
    resource_id: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get audit logs with optional filters"""
    audit_service = get_audit_service(db)
    logs = await audit_service.get_audit_logs(
        actor_id=actor_id,
        resource_id=resource_id,
        action=action,
        limit=limit,
    )
    return {"logs": logs}


@router.get("/agent/{agent_id}")
async def get_agent_audit_trail(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get complete audit trail for an agent"""
    audit_service = get_audit_service(db)
    logs = await audit_service.get_agent_audit_trail(agent_id)
    return {"agent_id": agent_id, "logs": logs}


@router.get("/resource/{resource_type}/{resource_id}")
async def get_resource_history(
    resource_type: str,
    resource_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get history of actions on a resource"""
    audit_service = get_audit_service(db)
    logs = await audit_service.get_resource_history(resource_type, resource_id)
    return {"resource_type": resource_type, "resource_id": resource_id, "logs": logs}
