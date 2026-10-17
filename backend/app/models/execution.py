"""Execution model"""

from sqlalchemy import Column, String, Text, Integer, Float, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from app.core.database import Base
from app.models.base import TimestampMixin


class ExecutionStatus(str, Enum):
    """Execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class Execution(Base, TimestampMixin):
    """Execution model"""
    
    __tablename__ = "executions"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    
    # Execution details
    status = Column(SQLEnum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False)
    input_data = Column(Text)  # JSON input
    output_data = Column(Text)  # JSON output
    error_message = Column(Text)
    
    # Metrics
    duration_seconds = Column(Float)
    total_tokens = Column(Integer, default=0)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    
    # Tool calls
    tool_call_count = Column(Integer, default=0)
    
    # Relationships
    agent = relationship("Agent", back_populates="executions")
    traces = relationship("Trace", back_populates="execution", cascade="all, delete-orphan")
