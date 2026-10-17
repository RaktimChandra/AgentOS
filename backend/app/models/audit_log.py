"""Audit log model"""

from sqlalchemy import Column, String, Text, JSON, ForeignKey
from app.core.database import Base
from app.models.base import TimestampMixin


class AuditLog(Base, TimestampMixin):
    """Audit log model for immutable audit trail"""
    
    __tablename__ = "audit_log"
    
    id = Column(String, primary_key=True, index=True)
    
    # Who
    user_id = Column(String, ForeignKey("users.id"), index=True)
    agent_id = Column(String, ForeignKey("agents.id"), index=True)
    
    # What
    action = Column(String, nullable=False, index=True)
    resource_type = Column(String, index=True)
    resource_id = Column(String, index=True)
    
    # Details
    details = Column(JSON)
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Policy decision
    policy_decision = Column(String)  # allow, deny, approve
    policy_reason = Column(Text)
