"""Trace model for OpenTelemetry spans"""

from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Trace(Base, TimestampMixin):
    """Trace model for storing OpenTelemetry spans"""
    
    __tablename__ = "traces"
    
    id = Column(String, primary_key=True, index=True)
    execution_id = Column(String, ForeignKey("executions.id"), nullable=False)
    trace_id = Column(String, index=True, nullable=False)
    span_id = Column(String, index=True, nullable=False)
    parent_span_id = Column(String, index=True)
    
    # Span details
    name = Column(String, nullable=False)
    kind = Column(String)  # span kind (internal, server, client, producer, consumer)
    start_time = Column(Float, nullable=False)  # Unix timestamp in seconds
    end_time = Column(Float)
    duration_ms = Column(Float)
    
    # Attributes (JSON)
    attributes = Column(JSON)
    
    # Status
    status_code = Column(Integer)
    status_message = Column(Text)
    
    # Relationships
    execution = relationship("Execution", back_populates="traces")
