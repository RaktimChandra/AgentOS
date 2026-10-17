"""Audit logging service"""

from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.audit_log import AuditLog
from app.models.user import User
from app.models.agent import Agent


class AuditService:
    """Service for audit logging"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log_action(
        self,
        actor_type: str,  # "user" or "agent"
        actor_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None,
        policy_decision: Optional[str] = None,
    ) -> AuditLog:
        """
        Log an action to the audit trail
        
        Args:
            actor_type: Type of actor (user or agent)
            actor_id: ID of the actor
            action: Action performed
            resource_type: Type of resource affected
            resource_id: ID of the resource
            details: Additional details
            policy_decision: Policy decision (allow/deny)
            
        Returns:
            Created audit log entry
        """
        import uuid
        
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            policy_decision=policy_decision,
            timestamp=datetime.utcnow(),
        )
        
        self.db.add(audit_log)
        await self.db.commit()
        await self.db.refresh(audit_log)
        
        return audit_log
    
    async def get_audit_logs(
        self,
        actor_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        """
        Get audit logs with optional filters
        
        Args:
            actor_id: Filter by actor ID
            resource_id: Filter by resource ID
            action: Filter by action
            limit: Maximum number of logs to return
            
        Returns:
            List of audit logs
        """
        query = select(AuditLog)
        
        if actor_id:
            query = query.where(AuditLog.actor_id == actor_id)
        
        if resource_id:
            query = query.where(AuditLog.resource_id == resource_id)
        
        if action:
            query = query.where(AuditLog.action == action)
        
        query = query.order_by(AuditLog.timestamp.desc()).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_agent_audit_trail(
        self,
        agent_id: str,
    ) -> list[AuditLog]:
        """
        Get complete audit trail for an agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            List of audit logs for the agent
        """
        return await self.get_audit_logs(actor_id=agent_id, limit=1000)
    
    async def get_resource_history(
        self,
        resource_type: str,
        resource_id: str,
    ) -> list[AuditLog]:
        """
        Get history of actions on a resource
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            
        Returns:
            List of audit logs for the resource
        """
        return await self.get_audit_logs(
            resource_type=resource_type,
            resource_id=resource_id,
            limit=1000,
        )


# Global audit service factory
def get_audit_service(db: AsyncSession) -> AuditService:
    """Get audit service instance"""
    return AuditService(db)
